import logging
import os
import sys

# Get the absolute path of the current directory
current_directory = os.path.abspath(os.path.dirname(__file__))

# Specify the absolute path for the log file
log_file_path = os.path.join(current_directory, 'test_log.log')

# Print the current directory and log file path
print(f"Current directory: {current_directory}")
print(f"Log file path: {log_file_path}")

# Ensure the log file directory is writable
if not os.access(current_directory, os.W_OK):
    print(f"Directory '{current_directory}' is not writable.")
    sys.exit(1)

# Configure logging with the absolute file path
logging.basicConfig(
    filename=log_file_path,
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s',
    filemode='w'  # Ensure the log file is overwritten each run
)

# Add a console handler to see logs in the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

# Check if logging is configured correctly
logger = logging.getLogger()
if not logger.hasHandlers():
    print("Logging is not configured properly.")
    sys.exit(1)

# Log a test message to verify the log file is being written
logging.info("This is a test log message.")

# Print completion message
print("Logging complete. Please check 'test_log.log' for details.")
