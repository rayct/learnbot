import json
import logging
import sys
from language_tool_python import LanguageTool
import enchant
import os

# Get the absolute path of the current directory
current_directory = os.path.abspath(os.path.dirname(__file__))

# Specify the absolute path for the log file
log_file_path = os.path.join(current_directory, 'json_duplicates.log')

# Ensure the log file directory is writable
if not os.access(current_directory, os.W_OK):
    print(f"Directory '{current_directory}' is not writable.")
    sys.exit(1)

# Configure logging with the absolute file path
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

# Print the log file path to confirm it's correct
print(f"Log file path: {log_file_path}")

# Check if logging is configured correctly
logger = logging.getLogger()
if not logger.hasHandlers():
    print("Logging is not configured properly.")
    sys.exit(1)

try:
    # Load JSON data
    print("Loading JSON data...")
    with open(os.path.join(current_directory, 'knowledge_base.json'), 'r') as file:
        data = json.load(file)
    print("JSON data loaded successfully.")
except FileNotFoundError:
    logging.error("File 'knowledge_base.json' not found. Please check the file path.")
    print("Error: File 'knowledge_base.json' not found. Please check the file path.")
    raise
except json.JSONDecodeError as e:
    logging.error(f"Error decoding JSON: {e}")
    print(f"Error decoding JSON: {e}")
    raise

# Initialize language tool for grammar checking
print("Initializing language tool...")
tool = LanguageTool('en-US')
print("Language tool initialized.")

# Initialize enchant for spell checking
print("Initializing spell checker...")
spell_checker = enchant.Dict("en_US")
print("Spell checker initialized.")

# Extract questions and answers
print("Extracting questions and answers...")
questions = [item['question'] for item in data['questions']]
answers = [item['answer'] for item in data['questions']]
print("Questions and answers extracted successfully.")

# Check for duplicate questions
print("Checking for duplicate questions...")
unique_questions = set()
duplicate_questions = set()

for question in questions:
    matches = tool.check(question)
    if matches or not spell_checker.check(question):
        logging.info(f"Potential error found in question: {question}")
    if question in unique_questions:
        duplicate_questions.add(question)
    else:
        unique_questions.add(question)
print("Duplicate questions check complete.")

# Check for duplicate answers
print("Checking for duplicate answers...")
unique_answers = set()
duplicate_answers = set()

for answer in answers:
    if answer in unique_answers:
        duplicate_answers.add(answer)
    else:
        unique_answers.add(answer)
print("Duplicate answers check complete.")

# Log results
if duplicate_questions:
    logging.info("Duplicate questions found:")
    for question in duplicate_questions:
        logging.info(question)
else:
    logging.info("No duplicate questions found.")

if duplicate_answers:
    logging.info("Duplicate answers found:")
    for answer in duplicate_answers:
        logging.info(answer)
else:
    logging.info("No duplicate answers found.")

# Close the logging system
logging.shutdown()

# Diagnostic message
print("Logging complete. Please check 'json_duplicates.log' for details.")
