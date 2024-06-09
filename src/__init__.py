# Initialization code for the 'src' package

# Importing the modules to make them available when the package is imported
from .chatbot import UKFormatter, load_knowledge_base, save_knowledge_base, find_best_match, \
    get_answer_for_question, get_user_input, add_new_answer, clear_log, chat_bot

# Setting up package-level variables or constants
VERSION = "1.0.0"
