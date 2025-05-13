import os
import mysql.connector
import json

def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

def search_word(english_word: str):
    try:
        db = connect_to_db()
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM words WHERE english_word = %s"
        cursor.execute(query, (english_word,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result
    except Exception as e:
        print("❌ MySQL Search Error:", e)
        return None

def insert_word_to_db(gpt_response: str):
    try:
        data = json.loads(gpt_response)
        db = connect_to_db()
        cursor = db.cursor()
        insert_query = """
            INSERT INTO words (english_word, word_meaning, azerbaijani_word)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
              word_meaning = VALUES(word_meaning),
              azerbaijani_word = VALUES(azerbaijani_word)
        """
        cursor.execute(insert_query, (
            data['english_word'], data['word_meaning'], data['azerbaijani_word']
        ))
        db.commit()
        cursor.close()
        db.close()
        print("✅ Inserted into DB")
    except Exception as e:
        print("❌ MySQL Insert Error:", e)
