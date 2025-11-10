from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection
import mysql.connector

app = Flask(__name__)
app.secret_key = "randomizerz"

# ---------- HOME ----------
@app.route("/")
def index():
    return render_template("index.html", title="Home")


# ---------- ABOUT ----------
@app.route("/about")
def about():
    return render_template("about.html", title="About")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and password == user["password"]:
            session["username"] = user["username"]
            session["fullname"] = user["full_name"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("index"))
        else:
            return render_template("loginpage.html", error="Invalid username or password")

    return render_template("loginpage.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        # Temporarily save info for verification
        session["signup_data"] = {
            "fullname": fullname,
            "username": username,
            "password": password
        }

        # Redirect to slider verification
        return redirect(url_for("slider_verification"))

    return render_template("signup.html")


# ---------- SLIDER VERIFICATION ----------
@app.route("/slider_verification", methods=["GET", "POST"])
def slider_verification():
    if request.method == "POST":
        signup_data = session.get("signup_data")

        if not signup_data:
            flash("Session expired. Please register again.")
            return redirect(url_for("signup"))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, username, password, role) VALUES (%s, %s, %s, %s)",
            (signup_data["fullname"], signup_data["username"], signup_data["password"], "user")
        )
        conn.commit()
        cursor.close()
        conn.close()

        # Clear session after successful registration
        session.pop("signup_data", None)

        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))

    return render_template("slider_verification.html", title="Verification")


# ---------- ADMIN DASHBOARD ----------
@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin_dashboard.html", title="Admin Dashboard")


# ---------- MANAGE ACCOUNTS ----------
@app.route("/manage_accounts")
def manage_accounts():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("manage_accounts.html", users=users, title="Manage Accounts")


@app.route("/delete_account/<int:user_id>")
def delete_account(user_id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("manage_accounts"))


@app.route("/edit_account/<int:user_id>", methods=["GET", "POST"])
def edit_account(user_id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        full_name = request.form.get("full_name")
        password = request.form.get("password")
        role = request.form.get("role")

        cursor.execute("""
            UPDATE users SET full_name=%s, password=%s, role=%s WHERE id=%s
        """, (full_name, password, role, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("manage_accounts"))

    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("edit_account.html", user=user)


# ---------- BOOK LIBRARY ----------
@app.route("/books")
def books():
    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    per_page = 3
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        cursor.execute("""
            SELECT COUNT(*) AS total 
            FROM books 
            WHERE book_name LIKE %s OR author_name LIKE %s
        """, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT COUNT(*) AS total FROM books")

    total_books = cursor.fetchone()["total"]
    total_pages = (total_books + per_page - 1) // per_page

    if search:
        cursor.execute("""
            SELECT * FROM books 
            WHERE book_name LIKE %s OR author_name LIKE %s 
            LIMIT %s OFFSET %s
        """, (f"%{search}%", f"%{search}%", per_page, offset))
    else:
        cursor.execute("SELECT * FROM books LIMIT %s OFFSET %s", (per_page, offset))

    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "book_library.html",
        title="Book Library",
        books=books,
        page=page,
        total_pages=total_pages,
        search=search
    )


# ---------- MANAGE REQUESTS ----------
@app.route("/manage_requests")
def manage_requests():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("manage_requests.html", title="Manage Requests")


# ---------- MANAGE WEBSITE ----------
@app.route("/manage_website")
def manage_website():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("manage_website.html", title="Manage Website")


# ---------- ADD BOOK ----------
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        book_name = request.form.get("book_name")
        author_name = request.form.get("author_name")
        content = request.form.get("content")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (book_name, author_name, content)
            VALUES (%s, %s, %s)
        """, (book_name, author_name, content))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("books"))

    return render_template("add_book.html", title="Add Book")


# ---------- EDIT BOOKS ----------
@app.route("/edit_books", methods=["GET", "POST"])
def edit_books():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        book_id = request.form.get("book_id")
        book_name = request.form.get("book_name")
        author_name = request.form.get("author_name")
        content = request.form.get("content")

        cursor.execute("""
            UPDATE books
            SET book_name = %s, author_name = %s, content = %s
            WHERE id = %s
        """, (book_name, author_name, content, book_id))
        conn.commit()

    search = request.args.get("search", "").strip()
    if search:
        cursor.execute("""
            SELECT * FROM books
            WHERE book_name LIKE %s OR author_name LIKE %s
        """, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("edit_books.html", books=books, title="Edit Books", search=search)


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
