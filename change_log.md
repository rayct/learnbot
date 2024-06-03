# Change Log

## [Added] Enhanced Matching Algorithm using spaCy

- Integrated spaCy library for more sophisticated matching algorithm.
- Installed spaCy and downloaded English language model.
- Used spaCy to compute similarity between user input and existing questions in the knowledge base.
- Replaced the `find_best_match` function with a new implementation that uses spaCy for similarity comparison.
- Improved accuracy of matching based on semantic similarity.

## [Changed] Logging Configuration

- Configured additional file handler for the existing `reboot_logger` to write log messages to the same log file (`chatbot.log`) as the general logging.
- All log messages, including those from the reboot process, are now written to the same log file.

## [Fixed] Reboot Process Error Handling

- Modified the reboot process to read the entire script content at once and execute it, avoiding syntax errors from partial code execution.
- Ensured that the reboot process is properly logged and executed without encountering syntax errors due to incomplete code execution.

## Added logging timestamps to UK/GB.

## Reversed the format from %Y-%m-%d (which represents YYYY-MM-DD) to %d-%m-%Y (which represents DD-MM-YYYY)

---

## Custom logging `Formatter` class, `UKFormatter`, is designed to convert timestamps to the London timezone and format the time in a specific way. Here's a review and some improvements to ensure clarity and correctness:

1. **Imports**: Ensure all necessary modules are imported.
2. **Use of Timezone**: The `timezone` function from the `pytz` module should be correctly imported and utilized.
3. **Handling Edge Cases**: Include handling for edge cases and errors.

Revised version of `UKFormatter` class:

```python
import logging
from datetime import datetime
import pytz

class UKFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        return dt.astimezone(pytz.timezone('Europe/London'))

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            s = dt.strftime("%d-%m-%Y %H:%M:%S")
        return s

# Example usage
if __name__ == "__main__":
    logger = logging.getLogger('example_logger')
    handler = logging.StreamHandler()
    handler.setFormatter(UKFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.info("This is a test log message.")
```

### Key Points:

1. **Imports**: Ensure you import `pytz` for timezone conversions.
   ```python
   import pytz
   ```

2. **Converter Function**: The `converter` function converts the timestamp to UTC and then to the `Europe/London` timezone.
   ```python
   def converter(self, timestamp):
       dt = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
       return dt.astimezone(pytz.timezone('Europe/London'))
   ```

3. **Formatting Time**: The `formatTime` function uses the converter and formats the time according to the specified or default format.
   ```python
   def formatTime(self, record, datefmt=None):
       dt = self.converter(record.created)
       if datefmt:
           s = dt.strftime(datefmt)
       else:
           s = dt.strftime("%d-%m-%Y %H:%M:%S")
       return s
   ```

4. **Example Usage**: Demonstrates how to set up the logger and use the custom formatter.
   ```python
   if __name__ == "__main__":
       logger = logging.getLogger('example_logger')
       handler = logging.StreamHandler()
       handler.setFormatter(UKFormatter())
       logger.addHandler(handler)
       logger.setLevel(logging.DEBUG)

       logger.info("This is a test log message.")
   ```

With this setup, any log messages created by `example_logger` will have their timestamps converted to the `Europe/London` timezone and formatted according to the specified or default format.

---

## Converted the logging timestamps to the UK/GB time zone in Python, you can use the pytz library to handle time zone conversions.

To ensure that the timestamps in your logging output are in the UK/GB time zone, you can use a custom formatter as previously described. This custom formatter will convert timestamps to the UK time zone before logging them. Here's how you can integrate this into your `app.py` script:

```python
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
            s = dt.strftime("%Y-%m-%d %H:%M:%S")
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
    for question in questions:
        similarity = nlp(user_input).similarity(nlp(question))
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
```

In this updated `app.py` script:

1. The `UKFormatter` class is used to format timestamps in the UK time zone.
2. `general_formatter` is an instance of `UKFormatter` used in the root logger's configuration.
3. The `reboot_logger` also uses an instance of `UKFormatter`.

This ensures that all log entries in `chatbot.log` have their timestamps converted to the UK time zone.