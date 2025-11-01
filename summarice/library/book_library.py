import mysql.connector
import sys
import json
import traceback
import urllib.parse

def add_book(book_name, author_name, content):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="summarice_db"
        )
        cursor = conn.cursor()

        sql = "INSERT INTO books (book_name, author_name, content) VALUES (%s, %s, %s)"
        values = (book_name, author_name, content)
        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        print(json.dumps({"status": "success"}))

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }))

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            # Expect one encoded argument
            encoded = sys.argv[1]
            decoded = urllib.parse.parse_qs(encoded)

            book_name = decoded.get("book_name", [""])[0]
            author_name = decoded.get("author_name", [""])[0]
            content = decoded.get("content", [""])[0]

            add_book(book_name, author_name, content)
        else:
            print(json.dumps({
                "status": "error",
                "message": f"Invalid arguments: {sys.argv}"
            }))
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }))

# ✅ Force flush output to PHP immediately
sys.stdout.flush()
