import json
import logging
import sys
import spacy
from typing import Optional, List, Dict, Any
from difflib import get_close_matches

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Configure general logging to existing log file
logging.basicConfig(
    filename='chatbot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configure reboot logging to existing log file
reboot_logger = logging.getLogger('reboot_logger')
reboot_handler = logging.FileHandler('chatbot.log')  # Using the same log file as general logging
reboot_handler.setLevel(logging.INFO)
reboot_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
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


# Remaining functions remain unchanged
