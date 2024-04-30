import json
from difflib import get_close_matches
from typing import Optional, List

def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: Knowledge base file '{file_path}' not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{file_path}': {e}")
        return {}

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
    matches: List[str] = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> Optional[str]:
    for q in knowledge_base.get("questions", []):
        if q.get("question") == question:
            return q.get("answer")
    return None


def get_user_input() -> str:
    return input('You: ')


def add_new_answer(knowledge_base: dict, user_input: str, new_answer: str):
    knowledge_base.setdefault("questions", []).append({"question": user_input, "answer": new_answer})
    save_knowledge_base('knowledge_base.json', knowledge_base)
    print('Bot: Thank you! I learned a new response!')


def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = get_user_input()

        if user_input.lower() == 'quit':
            break

        best_match: Optional[str] = find_best_match(user_input, [q.get("question", "") for q in knowledge_base.get("questions", [])])

        if best_match:
            answer: Optional[str] = get_answer_for_question(best_match, knowledge_base)
            if answer:
                print(f'Bot: {answer}')
            else:
                print('Bot: Sorry, I don\'t know the answer. Can you please educate me?')
                new_answer: str = input('Type the answer or "skip" to skip: ')
                if new_answer.lower() != 'skip':
                    add_new_answer(knowledge_base, user_input, new_answer)
        else:
            print('Bot: Sorry, I don\'t know the answer. Can you please educate me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')
            if new_answer.lower() != 'skip':
                add_new_answer(knowledge_base, user_input, new_answer)


if __name__ == '__main__':
    chat_bot()
