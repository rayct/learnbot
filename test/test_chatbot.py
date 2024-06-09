import unittest
from unittest.mock import patch, mock_open
import json
import logging
from io import StringIO
import sys

# Assume the chatbot code is in a module named chatbot
import src.chatbot as chatbot

class TestChatBot(unittest.TestCase):
    def setUp(self):
        # Mocking the logging
        self.log_stream = StringIO()
        logging.basicConfig(stream=self.log_stream, level=logging.INFO)

        # Configure test logging to file
        self.test_log_file = 'unit_test.log'
        self.file_handler = logging.FileHandler(self.test_log_file)
        self.file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(self.file_handler)

    def tearDown(self):
        logging.getLogger().removeHandler(self.file_handler)
        self.file_handler.close()

    @patch('builtins.input', side_effect=['What are your contact details please', 'quit'])
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "questions": [
            {
                "question": "What are your contact details please",
                "answer": "Our contact details are as follows\nPhone: 07972 612 395\nEmail: info@tailoredscaffolding.com\nWebsite: www.tailoredscaffolding.co.uk"
            }
        ]
    }))
    def test_normal_interaction(self, mock_open, mock_input):
        chatbot.chat_bot()
        output = self.log_stream.getvalue()
        self.assertIn("Best match for user input 'What are your contact details please' is 'What are your contact details please' with similarity 1.0.", output)
        self.assertIn("Responding to question 'What are your contact details please' with answer 'Our contact details are as follows", output)

    @patch('builtins.input', side_effect=['How do I reset my password?', 'You can reset your password by...', 'quit'])
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "questions": [
            {
                "question": "What are your contact details please",
                "answer": "Our contact details are as follows\nPhone: 07972 612 395\nEmail: info@tailoredscaffolding.com\nWebsite: www.tailoredscaffolding.co.uk"
            }
        ]
    }))
    def test_unknown_question_handling(self, mock_open, mock_input):
        chatbot.chat_bot()
        output = self.log_stream.getvalue()
        self.assertIn("No match found for the user question 'How do I reset my password?'", output)
        self.assertIn("New answer added for question 'How do I reset my password?'", output)

    @patch('builtins.input', side_effect=['reload', 'quit'])
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "questions": [
            {
                "question": "What are your contact details please",
                "answer": "Our contact details are as follows\nPhone: 07972 612 395\nEmail: info@tailoredscaffolding.com\nWebsite: www.tailoredscaffolding.co.uk"
            }
        ]
    }))
    def test_reload_command(self, mock_open, mock_input):
        chatbot.chat_bot()
        output = self.log_stream.getvalue()
        self.assertIn("Knowledge base reloaded by Ray.", output)

    @patch('builtins.input', side_effect=['reboot'])
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "questions": [
            {
                "question": "What are your contact details please",
                "answer": "Our contact details are as follows\nPhone: 07972 612 395\nEmail: info@tailoredscaffolding.com\nWebsite: www.tailoredscaffolding.co.uk"
            }
        ]
    }))
    @patch('chatbot.sys.argv', ['chatbot.py'])
    def test_reboot_command(self, mock_open, mock_input, mock_argv):
        with patch('chatbot.open', mock_open(read_data=open('chatbot.py').read())), patch('chatbot.exec') as mock_exec:
            chatbot.chat_bot()
            output = self.log_stream.getvalue()
            self.assertIn("Chatbot reboot initiated by Ray.", output)
            self.assertIn("Rebooting the chatbot program.", output)
            mock_exec.assert_called_once()

    @patch('builtins.input', side_effect=['quit'])
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "questions": [
            {
                "question": "What are your contact details please",
                "answer": "Our contact details are as follows\nPhone: 07972 612 395\nEmail: info@tailoredscaffolding.com\nWebsite: www.tailoredscaffolding.co.uk"
            }
        ]
    }))
    def test_quit_command(self, mock_open, mock_input):
        chatbot.chat_bot()
        output = self.log_stream.getvalue()
        self.assertIn("Chatbot session ended by Ray.", output)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_file_not_found_error(self, mock_open):
        chatbot.chat_bot()
        output = self.log_stream.getvalue()
        self.assertIn("Knowledge base file 'knowledge_base.json' not found.", output)

    @patch('builtins.open', new_callable=mock_open, read_data='{ invalid json }')
    def test_json_decode_error(self, mock_open):
        chatbot.chat_bot()
        output = self.log_stream.getvalue()
        self.assertIn("Error decoding JSON in file 'knowledge_base.json'", output)

    @patch('chatbot.logging.critical')
    def test_unexpected_error(self, mock_critical):
        with patch('chatbot.get_user_input', side_effect=Exception('Unexpected error')):
            chatbot.chat_bot()
            mock_critical.assert_called_once_with('Critical error in main execution: Unexpected error')

if __name__ == '__main__':
    unittest.main()
