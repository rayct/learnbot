import os

# Get the absolute path of the current directory
current_directory = os.path.abspath(os.path.dirname(__file__))

# Specify the path for the test file
test_file_path = os.path.join(current_directory, 'test_write_permissions.log')
log_copy_path = os.path.join(current_directory, 'write_permission_test_copy.log')

try:
    # Try to create and write to the test file
    with open(test_file_path, 'w') as test_file:
        test_file.write("This is a test file to check write permissions.\n")
    print(f"Successfully wrote to {test_file_path}")

    # Optionally, read back the file to confirm
    with open(test_file_path, 'r') as test_file:
        content = test_file.read()
        print("Content of the test file:")
        print(content)

    # Copy the test file content to the log copy path
    with open(log_copy_path, 'w') as log_copy_file:
        log_copy_file.write(content)
    print(f"A copy of the log has been saved to {log_copy_path}")

except IOError as e:
    print(f"Failed to write to {test_file_path}: {e}")

finally:
    # Clean up: delete the test file if it was created
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
        print(f"Deleted test file {test_file_path}")

