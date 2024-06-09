### Test Procedure for Chatbot Application

#### 1. Environment Setup
- Ensure Python 3.x is installed on the system.
- Install required dependencies:
  ```sh
  pip install spacy pytz
  python -m spacy download en_core_web_md
  ```

#### 2. Test Configuration
- Create a file named `knowledge_base.json` with initial test data:
  ```json
  {
    "questions": [
      {
        "question": "What are your contact details please",
        "answer": "Our contact details are as follows\nPhone: 07972 612 395\nEmail: info@tailoredscaffolding.com\nWebsite: www.tailoredscaffolding.co.uk"
      }
    ]
  }
  ```
- Ensure the script is saved as `chatbot.py`.

#### 3. Test Cases

##### 3.1 Initialization and Logging

1. **Start the application:**
   ```sh
   python chatbot.py
   ```
2. **Verify logs:**
   - Check `chatbot.log` for a successful start message:
     ```
     [timestamp] - INFO - Knowledge base loaded successfully.
     ```

##### 3.2 User Interaction

3. **Normal Interaction:**
   - Input: `What are your contact details please`
   - Expected Output: `Bot: Our contact details are as follows...`
   - Verify logs:
     ```
     [timestamp] - INFO - Best match for user input 'What are your contact details please' is 'What are your contact details please' with similarity 1.0.
     [timestamp] - INFO - Responding to question 'What are your contact details please' with answer 'Our contact details are as follows...'.
     ```

4. **Unknown Question Handling:**
   - Input: `How do I reset my password?`
   - Expected Output: `Bot: Sorry, I don't know the answer. Can you please educate me?`
   - Input new answer: `You can reset your password by...`
   - Expected Output: `Bot: Thank you! I learned a new response!`
   - Verify `knowledge_base.json` is updated with the new Q&A.
   - Verify logs:
     ```
     [timestamp] - WARNING - No match found for the user question 'How do I reset my password?'.
     [timestamp] - INFO - New answer added for question 'How do I reset my password?'.
     ```

##### 3.3 Commands

5. **Reload Command:**
   - Input: `reload`
   - Expected Output: `Bot: Knowledge base reloaded.`
   - Verify logs:
     ```
     [timestamp] - INFO - Knowledge base reloaded by Ray.
     ```

6. **Reboot Command:**
   - Input: `reboot`
   - Expected Output: `Bot: Rebooting...`
   - Verify logs:
     ```
     [timestamp] - INFO - Chatbot reboot initiated by Ray.
     [timestamp] - INFO - Reboot process started.
     [timestamp] - INFO - Rebooting the chatbot program.
     ```

7. **Quit Command:**
   - Input: `quit`
   - Expected Output: `Bot: Goodbye!`
   - Verify logs:
     ```
     [timestamp] - INFO - Chatbot session ended by Ray.
     ```

##### 3.4 Error Handling

8. **File Not Found Error:**
   - Delete or rename `knowledge_base.json`.
   - Start the application.
   - Expected Output: `Bot: An unexpected error occurred. Please try again.`
   - Verify logs:
     ```
     [timestamp] - ERROR - Knowledge base file 'knowledge_base.json' not found.
     ```

9. **JSON Decode Error:**
   - Corrupt `knowledge_base.json` content.
   - Start the application.
   - Expected Output: `Bot: An unexpected error occurred. Please try again.`
   - Verify logs:
     ```
     [timestamp] - ERROR - Error decoding JSON in file 'knowledge_base.json': [error details]
     ```

##### 3.5 Unexpected Errors

10. **Simulate Unexpected Error:**
    - Modify the code to introduce an error (e.g., undefined variable).
    - Start the application.
    - Expected Output: `Bot: A critical error occurred. Exiting...`
    - Verify logs:
      ```
      [timestamp] - CRITICAL - Critical error in main execution: [error details]
      ```

---

Below is a full test code that automates the testing of the chatbot application. This test code uses the `unittest` framework and the `unittest.mock` module to simulate user inputs and outputs.

To integrate the provided test code with the chatbot application, you can name the test file `test_chatbot.py`. This naming convention follows the typical practice for naming test files in Python projects and makes it clear that this file contains tests for the `chatbot.py` module.

Here's how you can organize your files:

```
project_directory/
    chatbot.py
    test_chatbot.py
    knowledge_base.json
    chatbot.log
    unit_test.log
```

- `chatbot.py`: The main chatbot application script.
- `test_chatbot.py`: The test script containing the unit tests.
- `knowledge_base.json`: The knowledge base file used by the chatbot.
- `chatbot.log`: The log file for general and reboot logs.
- `unit_test.log`: The log file for capturing logs generated during unit tests.

### Running the Tests

To run the tests, navigate to the directory containing these files and execute the following command in your terminal or command prompt:

```sh
python -m unittest test_chatbot.py
```

This command will execute all the test cases defined in `test_chatbot.py` and generate logs in `unit_test.log`.

### Full Test Code in `test_chatbot.py`

Here is the complete `test_chatbot.py` file content:

```python
import unittest
from unittest.mock import patch, mock_open
import json
import logging
from io import StringIO
import sys

# Assume the chatbot code is in a module named chatbot
import chatbot

class TestChatBot(unittest.TestCase):
    def setUp(self):
        # Set up a sample knowledge base
        self.sample_knowledge_base = {
            "questions": [
                {
                    "question": "What are your contact details please",
                    "answer": "Our contact details are as follows\nPhone: 07972 612 395\nEmail: info@tailoredscaffolding.com\nWebsite: www.tailoredscaffolding.co.uk"
                }
            ]
        }

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
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(self.sample_knowledge_base))
    def test_normal_interaction(self, mock_open, mock_input):
        chatbot.chat_bot()
        output = self.log_stream.getvalue()
        self.assertIn("Best match for user input 'What are your contact details please' is 'What are your contact details please' with similarity 1.0.", output)
        self.assertIn("Responding to question 'What are your contact details please' with answer 'Our contact details are as follows", output)

    @patch('builtins.input', side_effect=['How do I reset my password?', 'You can reset your password by...', 'quit'])
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(self.sample_knowledge_base))
    def test_unknown_question_handling(self, mock_open, mock_input):
        chatbot.chat_bot()
        output = self.log_stream.getvalue()
        self.assertIn("No match found for the user question 'How do I reset my password?'", output)
        self.assertIn("New answer added for question 'How do I reset my password?'", output)

    @patch('builtins.input', side_effect=['reload', 'quit'])
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(self.sample_knowledge_base))
    def test_reload_command(self, mock_open, mock_input):
        chatbot.chat_bot()
        output = self.log_stream.getvalue()
        self.assertIn("Knowledge base reloaded by Ray.", output)

    @patch('builtins.input', side_effect=['reboot'])
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(self.sample_knowledge_base))
    @patch('chatbot.sys.argv', ['chatbot.py'])
    def test_reboot_command(self, mock_open, mock_input, mock_argv):
        with patch('chatbot.open', mock_open(read_data=open('chatbot.py').read())), patch('chatbot.exec') as mock_exec:
            chatbot.chat_bot()
            output = self.log_stream.getvalue()
            self.assertIn("Chatbot reboot initiated by Ray.", output)
            self.assertIn("Rebooting the chatbot program.", output)
            mock_exec.assert_called_once()

    @patch('builtins.input', side_effect=['quit'])
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(self.sample_knowledge_base))
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
```

### Running the Tests

Execute the test suite using the following command in your terminal or command prompt:

```sh
python -m unittest test_chatbot.py
```

This will run all the defined test cases, and the logs generated during the test execution will be stored in `unit_test.log`. You can then open `unit_test.log` to review the detailed logs.







### Conclusion
By following this test procedure, you can systematically verify the functionality, error handling, and logging of the chatbot application. Make sure to document the results for each test case to ensure the application meets the expected behavior.