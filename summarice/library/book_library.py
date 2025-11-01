import mysql.connector
import json
import traceback

def get_books():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="summarice_db"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, book_name AS title, author_name AS author, content FROM books"
        )
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return books
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}


if __name__ == "__main__":
    try:
        books = get_books()
        print(json.dumps(books, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e), "trace": traceback.format_exc()}))
