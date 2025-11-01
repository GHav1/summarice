import mysql.connector
import json
import sys

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
        # Print JSON error for PHP to read
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    books = get_books()
    # ✅ Always print pure JSON output (no extra text)
    print(json.dumps(books, ensure_ascii=False))

