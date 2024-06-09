import json
import mysql.connector
from mysql.connector import Error

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def connect_to_database(host, database, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def insert_questions(connection, questions):
    cursor = connection.cursor()
    for q in questions:
        question = q['question']
        answer = q['answer']
        try:
            cursor.execute(
                "INSERT INTO questions (question, answer) VALUES (%s, %s)",
                (question, answer)
            )
        except Error as e:
            print(f"Error: {e}")

    connection.commit()
    cursor.close()

def main():
    # Load the JSON data
    questions_data = load_json('intents.json')

    # Connect to the MySQL database
    connection = connect_to_database(
        host='your_host',
        database='your_database',
        user='your_username',
        password='your_password'
    )

    if connection:
        # Insert questions into the database
        insert_questions(connection, questions_data['questions'])
        connection.close()
        print("Data inserted successfully and connection closed")

if __name__ == "__main__":
    main()
