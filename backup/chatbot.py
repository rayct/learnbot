import json
import logging
import sys
import spacy
from typing import Optional, List, Dict, Any
from datetime import datetime
from pytz import timezone, UTC

# Load spaCy model
nlp = spacy.load("en_core_web_md")

class UKFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp, tz=UTC)
        return dt.astimezone(timezone('Europe/London'))

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            s = dt.strftime("%d-%m-%Y %H:%M:%S")
        return s

# Configure general logging to existing log file
general_formatter = UKFormatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.basicConfig(
    filename='chatbot.log',
    level=logging.INFO
)

# Apply the UKFormatter to the root logger's handlers
for handler in logging.getLogger().handlers:
    handler.setFormatter(general_formatter)

# Configure reboot logging to existing log file
reboot_logger = logging.getLogger('reboot_logger')
reboot_handler = logging.FileHandler('chatbot.log')  # Using the same log file as general logging
reboot_handler.setLevel(logging.INFO)
reboot_handler.setFormatter(UKFormatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
reboot_logger.addHandler(reboot_handler)

def load_knowledge_base(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r') as file:
            data: Dict[str, Any] = json.load(file)
        logging.info("Knowledge base loaded successfully.")
        return data
    except FileNotFoundError:
        logging.error(f"Knowledge base file '{file_path}' not found.")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in file '{file_path}': {e}")
        return {}

def save_knowledge_base(file_path: str, data: Dict[str, Any]):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
        logging.info("Knowledge base saved successfully.")
    except Exception as e:
        logging.error(f"Error saving knowledge base to '{file_path}': {e}")

def find_best_match(user_input: str, questions: List[str]) -> Optional[str]:
    best_match = None
    max_similarity = 0.0
    user_doc = nlp(user_input)
    
    if not user_doc.vector_norm:  # Check if the user input vector is not empty
        logging.warning(f"User input '{user_input}' resulted in an empty vector.")
        return None

    for question in questions:
        question_doc = nlp(question)
        
        if not question_doc.vector_norm:  # Check if the question vector is not empty
            logging.warning(f"Question '{question}' resulted in an empty vector.")
            continue
        
        similarity = user_doc.similarity(question_doc)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = question
    
    logging.info(f"Best match for user input '{user_input}' is '{best_match}' with similarity {max_similarity}.")
    return best_match if max_similarity > 0.6 else None

def get_answer_for_question(question: str, knowledge_base: Dict[str, Any]) -> Optional[str]:
    for q in knowledge_base.get("questions", []):
        if q.get("question") == question:
            return q.get("answer")
    return None

def get_user_input() -> str:
    try:
        return input('You: ')
    except KeyboardInterrupt:
        logging.info("User initiated exit.")
        raise

def add_new_answer(knowledge_base: Dict[str, Any], user_question: str, new_answer: str):
    knowledge_base.setdefault("questions", []).append({"question": user_question, "answer": new_answer})
    save_knowledge_base('knowledge_base.json', knowledge_base)
    logging.info(f"New answer added for question '{user_question}'.")
    print('Bot: Thank you! I learned a new response!')

def clear_log():
    try:
        open('chatbot.log', 'w').close()
        logging.info("Log file cleared successfully.")
        print('Log file cleared successfully.')
    except Exception as e:
        logging.error(f"Error clearing log file: {e}")
        print('Error clearing log file.')

def chat_bot():
    knowledge_base_file = 'knowledge_base.json'
    knowledge_base: Dict[str, Any] = load_knowledge_base(knowledge_base_file)

    while True:
        try:
            user_input: str = get_user_input()

            if user_input.lower() == 'quit':
                logging.info("Chatbot session ended by Ray.")
                print('\nBot: Goodbye!')
                break
            elif user_input.lower() == 'exit':
                logging.info("Chatbot session ended by Ray.")
                print('\nBot: Goodbye!')
                break
            elif user_input.lower() == 'reload':
                knowledge_base = load_knowledge_base(knowledge_base_file)
                print('Bot: Knowledge base reloaded.')
                logging.info("Knowledge base reloaded by Ray.")
                continue
            elif user_input.lower() == 'reboot':
                logging.info("Chatbot reboot initiated by Ray.")
                reboot_logger.info("Reboot process started.")
                try:
                    print('Bot: Rebooting...')
                    reboot_logger.info("Rebooting the chatbot program.")

                    # Open the current script and read it all at once
                    with open(sys.argv[0], 'r') as script_file:
                        script_content = script_file.read()
                        reboot_logger.info(script_content)
                        exec(script_content)

                    reboot_logger.info("Chatbot reboot completed successfully.")
                except Exception as e:
                    reboot_logger.error(f"Error during reboot: {e}")
                    print('Bot: An error occurred during reboot.')
                break
            elif user_input.lower() == 'clear log':
                clear_log()
                continue

            questions_list = [q.get("question", "") for q in knowledge_base.get("questions", [])]
            best_match: Optional[str] = find_best_match(user_input, questions_list)

            if best_match:
                answer: Optional[str] = get_answer_for_question(best_match, knowledge_base)
                if answer:
                    logging.info(f"Responding to question '{best_match}' with answer '{answer}'.")
                    print(f'Bot: {answer}')
                else:
                    logging.warning(f"No answer found for the matched question '{best_match}'.")
                    print('Bot: Sorry, I don\'t know the answer. Can you please educate me?')
                    new_answer: str = input('Type the answer or "skip" to skip: ')
                    if new_answer.lower() != 'skip':
                        add_new_answer(knowledge_base, user_input, new_answer)
            else:
                logging.warning(f"No match found for the user question '{user_input}'.")
                print('Bot: Sorry, I don\'t know the answer. Can you please educate me?')
                new_answer: str = input('Type the answer or "skip" to skip: ')
                if new_answer.lower() != 'skip':
                    add_new_answer(knowledge_base, user_input, new_answer)

        except KeyboardInterrupt:
            logging.info("Chatbot session interrupted by Ray.")
            print('\nBot: Goodbye!')
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print('Bot: An unexpected error occurred. Please try again.')

if __name__ == '__main__':
    try:
        chat_bot()
    except Exception as e:
        logging.critical(f"Critical error in main execution: {e}")
        print('Bot: A critical error occurred. Exiting...')

