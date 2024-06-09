import json
import logging
from language_tool_python import LanguageTool
import enchant

# Configure logging
logging.basicConfig(filename='json_duplicates.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load JSON data
with open('knowledge_base.json', 'r') as file:
    data = json.load(file)

# Initialize language tool for grammar checking
tool = LanguageTool('en-US')

# Initialize enchant for spell checking
spell_checker = enchant.Dict("en_US")

# Extract questions and answers
questions = [item['question'] for item in data['questions']]
answers = [item['answer'] for item in data['questions']]

# Check for duplicate questions
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

# Check for duplicate answers
unique_answers = set()
duplicate_answers = set()

for answer in answers:
    if answer in unique_answers:
        duplicate_answers.add(answer)
    else:
        unique_answers.add(answer)

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
