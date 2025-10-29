import mysql.connector

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
        return "Book added successfully!"
    except Exception as e:
        return f"Error: {e}"
