from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection
import mysql.connector

app = Flask(__name__)
app.secret_key = "randomizerz"


# ---------- Home ----------
@app.route("/")
def index():
    return render_template("index.html", title="Home")


# ---------- About ----------
@app.route("/about")
def about():
    return render_template("about.html", title="About")


# ---------- Login ----------
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
            # Store user info in session
            session["username"] = user["username"]
            session["fullname"] = user["full_name"]
            session["role"] = user["role"]

            # Redirect based on role
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("index"))
        else:
            return render_template("loginpage.html", error="Invalid username or password")

    return render_template("loginpage.html")


# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- Signup ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, username, password, role) VALUES (%s, %s, %s, %s)",
            (fullname, username, password, "user"),
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------- Admin Dashboard ----------
@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin_dashboard.html", title="Admin Dashboard")


# ---------- Manage Accounts ----------
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


# ---------- Book Library ----------
@app.route("/books")
def books():
    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    per_page = 3
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # --- Count total books ---
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

    # --- Fetch books ---
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


# ---------- Manage Requests ----------
@app.route("/manage_requests")
def manage_requests():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("manage_requests.html", title="Manage Requests")


# ---------- Manage Website ----------
@app.route("/manage_website")
def manage_website():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("manage_website.html", title="Manage Website")

# Add Book
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



# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
