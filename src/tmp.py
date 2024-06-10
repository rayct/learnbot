import json
import sys
from language_tool_python import LanguageTool
import enchant
import os
from datetime import datetime

# Function to write log messages to a file with timestamps and line numbers
def write_log(message, line_number=None):
    log_file_path = 'json_duplicates.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file_path, 'a') as log_file:
        if line_number is not None:
            log_file.write(f"{timestamp} - Line {line_number}: {message}\n")
        else:
            log_file.write(f"{timestamp} - {message}\n")
    # Print the message to the terminal with timestamp and line number
    if line_number is not None:
        print(f"{timestamp} - Line {line_number}: {message}")
    else:
        print(f"{timestamp} - {message}")

# Function to load JSON data from a specified directory
def load_json_data(directory):
    try:
        write_log("Loading JSON data...")
        file_path = os.path.join(directory, 'knowledge_base.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        write_log("JSON data loaded successfully.")
        return data
    except FileNotFoundError:
        write_log(f"Error: File '{file_path}' not found. Please check the file path.")
        print(f"Error: File '{file_path}' not found. Please check the file path.")
        raise
    except json.JSONDecodeError as e:
        write_log(f"Error decoding JSON: {e}")
        print(f"Error decoding JSON: {e}")
        raise

# Log a message to indicate the script start
write_log("Script started.")

# Get the absolute path of the current directory
# Set the directory containing the knowledge_base.json file
knowledge_base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

# Load JSON data from the specified directory
data = load_json_data(knowledge_base_directory)

# data = load_json_data(custom_directory)
# data = load_json_data(current_directory)

# Initialize language tool for grammar checking
write_log("Initializing language tool...")
tool = LanguageTool('en-US')
write_log("Language tool initialized.")

# Initialize enchant for spell checking
write_log("Initializing spell checker...")
spell_checker = enchant.Dict("en_US")
write_log("Spell checker initialized.")

# Extract questions and answers
write_log("Extracting questions and answers...")
questions = [item['question'] for item in data['questions']]
answers = [item['answer'] for item in data['questions']]
write_log("Questions and answers extracted successfully.")

# Check for duplicate questions
write_log("Checking for duplicate questions...")
unique_questions = set()
duplicate_questions = set()

for line_number, question in enumerate(questions, start=1):
    matches = tool.check(question)
    if matches or not spell_checker.check(question):
        write_log(f"Potential error found in question: {question}", line_number)
    if question in unique_questions:
        duplicate_questions.add(question)
    else:
        unique_questions.add(question)
write_log("Duplicate questions check complete.")

# Check for duplicate answers
write_log("Checking for duplicate answers...")
unique_answers = set()
duplicate_answers = set()

for line_number, answer in enumerate(answers, start=1):
    if answer in unique_answers:
        duplicate_answers.add(answer)
    else:
        unique_answers.add(answer)
write_log("Duplicate answers check complete.")

# Log results for Duplicate Questions
if duplicate_questions:
    write_log(f"Duplicate questions found: {len(duplicate_questions)} errors found")
    for question in duplicate_questions:
        write_log(question)
else:
    write_log("No duplicate questions found.")

# Log results for Duplicate Answers
if duplicate_answers:
    write_log(f"Duplicate answers found: {len(duplicate_answers)} errors found")
    for answer in duplicate_answers:
        write_log(answer)
else:
    write_log("No duplicate answers found.")

# Log a message to indicate the script end
write_log("Script completed.")

# Diagnostic message
print("Logging complete. Please check 'json_duplicates.log' for details.")
