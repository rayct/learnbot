The `intents.json` file.

```json
{
  "questions": [
    {
      "question": "Hello",
      "answer": "Hi"
    },
    {
      "question": "Hi",
      "answer": "Hello, how may I help you?"
    },
    {
      "question": "What do your Scaffold hire rates start from?",
      "answer": "This will depend upon various factors, can you provide me with some more information please?"
    },
    {
      "question": "hi",
      "answer": "hi"
    },
    {
      "question": "What is 3 * 5",
      "answer": "3 * 5 is 15, Basically 3 multiplied by 5 = 15"
    },
    {
      "question": "What are your prices",
      "answer": "Prices start from \u00a3150 for an on-site quote and survey"
    },
    {
      "question": "I need a quote for some scaffolding",
      "answer": "Sure, can you provide me with some more details so I can assist you further?"
    },
    {
      "question": "It's for an extension on a bungalow",
      "answer": "Ok! are you able to provide the size and area of the bungalow"
    },
    {
      "question": "Scaffold hire prices",
      "answer": "Sure, Our prices depend on the type of scaffolding you require, you can contact us via email info@tailoredscaffolding.co.uk or phone on 08878026349 for a more detailed quote"
    },
    {
      "question": "How are you?",
      "answer": "I'm very well thank you for asking, how are you today?"
    },
    {
      "question": "I'm doing great",
      "answer": "I'm so glad to hear that you are doing great!"
    },
    {
      "question": "Can you tell jokes?",
      "answer": "Sure, Why don't scientists trust atoms? Because they make up everything!"
    },
    {
      "question": "Tell me another one",
      "answer": "OK, Why did the scarecrow win an award? Because he was outstanding in his field!"
    },
    {
      "question": "Anymore Jokes",
      "answer": "Absolutely, Why did the bicycle fall over? Because it was two-tired!"
    },
    {
      "question": "Are you an accredited installer?",
      "answer": "Yes we are, our scaffolders each hold their own accreditations such as the CISRS, CSCS and CHAS registered."
    },
    {
      "question": "prices",
      "answer": "Our prices vary depending on the scale of the job."
    },
    {
      "question": "I need scaffolding for a roofing project can you help?",
      "answer": "Sure, I can assist you with that. Could you provide me with some more information regarding the height and size of the building? For example, is it a house or a bungalow? How many levels does the building have, and for how long do you require the scaffold?"
    },
    {
      "question": "scaffold duration",
      "answer": "Scaffold duration depends on various factors such as project requirements."
    },
    {
      "question": "quote",
      "answer": "What are your requirements please so I may assist you further?"
    },
    {
      "question": "Hello there",
      "answer": "Hi, how may I help you?"
    },
    {
      "question": "quotes",
      "answer": "Yes I can provide quotes, can you provide some more information so I may assist you further?"
    }
  ]
}
```

### Loading the JSON into MySQL

Here is a Python script to load this JSON file into a MySQL database:

1. **Ensure the MySQL table schema**:
    ```sql
    CREATE TABLE questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    );
    ```

2. **Python script to load JSON data**:
    ```python
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
    ```

### Steps to Run the Script

1. **Create the MySQL table**: Run the SQL command to create the `questions` table.
2. **Save the JSON file**: Save your `intents.json` file in the same directory as the script.
3. **Run the Python script**: Execute the script to load the data into the database.

```sh
python load_intents.py
```

*Ensure you replace `'your_host'`, `'your_database'`, `'your_username'`, and `'your_password'` with your actual MySQL database credentials. This script will read the `intents.json` file, connect to your MySQL database, and insert each question and answer into the `questions` table.*

---

**Documentation By:** Raymond C. Turner

**Revision:** May 30th, 2024


**codestak.io**