import os

def clear_log(log_file_path):
    try:
        # Open the log file in write mode to clear its contents
        with open(log_file_path, 'w') as log_file:
            log_file.write('')
        print(f"Log file '{log_file_path}' cleared successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    log_file_path = input("Enter the path of the log file to clear: ").strip()

    # Check if the specified file exists
    if os.path.isfile(log_file_path):
        confirm = input(f"Are you sure you want to clear '{log_file_path}'? (yes/no): ").strip().lower()
        if confirm == 'yes':
            clear_log(log_file_path)
        else:
            print("Operation canceled.")
    else:
        print(f"Error: Log file '{log_file_path}' not found.")
