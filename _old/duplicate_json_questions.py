import json
import logging
from language_tool_python import LanguageTool
import enchant

# Configure logging
logging.basicConfig(filename='duplicate_questions.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load JSON data
with open('knowledge_base.json', 'r') as file:
    data = json.load(file)

# Initialize language tool for grammar checking
tool = LanguageTool('en-US')

# Initialize enchant for spell checking
spell_checker = enchant.Dict("en_US")

# Extract questions
questions = [item['question'] for item in data['questions']]

# Check for repeats
unique_questions = set()
duplicate_questions = set()

# Check for grammar and spell errors
for question in questions:
    matches = tool.check(question)
    if matches or not spell_checker.check(question):
        logging.info(f"Potential error found in question: {question}")
    if question in unique_questions:
        duplicate_questions.add(question)
    else:
        unique_questions.add(question)

# Log results
if duplicate_questions:
    logging.info("Duplicate questions found:")
    for question in duplicate_questions:
        logging.info(question)
else:
    logging.info("No duplicate questions found.")
