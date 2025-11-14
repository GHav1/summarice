from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "randomizerz"


# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html", title="Home")


# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html", title="About")


# ---------------- LOGIN ----------------
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

        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            session["fullname"] = user["full_name"]
            session["role"] = user["role"]
            session["user_id"] = user["id"]

            if user["role"] in ["admin", "superAdmin"]:
                return redirect(url_for("admin_dashboard"))

            return redirect(url_for("index"))

        return render_template("loginpage.html", error="Invalid username or password")

    return render_template("loginpage.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        session["signup_data"] = {
            "fullname": fullname,
            "username": username,
            "password": password
        }

        return redirect(url_for("slider_verification"))

    return render_template("signup.html")


# ---------------- SLIDER VERIFICATION ----------------
@app.route("/slider_verification", methods=["GET", "POST"])
def slider_verification():
    if request.method == "POST":
        data = session.get("signup_data")

        if not data:
            flash("Session expired. Please register again.")
            return redirect(url_for("signup"))

        hashed = generate_password_hash(data["password"])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (full_name, username, password, role)
            VALUES (%s, %s, %s, %s)
        """, (data["fullname"], data["username"], hashed, "user"))
        conn.commit()
        cursor.close()
        conn.close()

        session.pop("signup_data")

        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))

    return render_template("slider_verification.html")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin_dashboard():
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))
    return render_template("admin_dashboard.html", title="Admin Dashboard")


# ---------------- MANAGE ACCOUNTS ----------------
@app.route("/manage_accounts")
def manage_accounts():
    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    valid_columns = ["id", "full_name", "username", "role"]
    if sort_by not in valid_columns:
        sort_by = "id"

    if order not in ["asc", "desc"]:
        order = "asc"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = f"SELECT * FROM users ORDER BY {sort_by} {order}"
    cursor.execute(query)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "manage_accounts.html",
        users=users,
        sort_by=sort_by,
        order=order
    )

# DELETE ACCOUNT
@app.route("/delete_account/<int:user_id>")
def delete_account(user_id):
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("manage_accounts"))


# EDIT ACCOUNT
@app.route("/edit_account/<int:user_id>", methods=["GET", "POST"])
def edit_account(user_id):
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    return_to = request.args.get("return_to", "manage_accounts")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if request.method == "POST":
        fullname = request.form.get("full_name")
        role = request.form.get("role")

        cursor.execute("""
            UPDATE users SET full_name = %s, role = %s WHERE id = %s
        """, (fullname, role, user_id))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for(return_to))

    cursor.close()
    conn.close()

    return render_template("edit_account.html", user=user, return_to=return_to)


# RESET PASSWORD
@app.route("/reset_password/<int:user_id>")
def reset_password(user_id):
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    temp_password = "Summarice123"
    hashed = generate_password_hash(temp_password)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Temporary password set: {temp_password}")
    return redirect(url_for("manage_accounts"))


# ---------------- SUPER ADMIN ADVANCE ----------------
@app.route("/advance")
def advance():
    if session.get("role") != "superAdmin":
        return "Access denied", 403
    return render_template("advance.html")


@app.route("/advance_manage_accounts")
def advance_manage_accounts():
    if session.get("role") != "superAdmin":
        return redirect(url_for("login"))

    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    valid_columns = ["id", "full_name", "username", "role"]
    if sort_by not in valid_columns:
        sort_by = "id"

    if order not in ["asc", "desc"]:
        order = "asc"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = f"SELECT * FROM users ORDER BY {sort_by} {order}"
    cursor.execute(query)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "advance_manage_accounts.html",
        users=users,
        sort_by=sort_by,
        order=order
    )



# ---------------- CHANGE PASSWORD (users) ----------------
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetch user bsd sessh username
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (session['username'],))
    user = cursor.fetchone()

    if request.method == 'POST':
        current = request.form.get('current_password')
        new = request.form.get('new_password')
        confirm = request.form.get('confirm_password')

        if not check_password_hash(user['password'], current):
            return render_template("change_password.html", error="Incorrect current password")

        if new != confirm:
            return render_template("change_password.html", error="Passwords do not match")

        new_hashed = generate_password_hash(new)
        cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new_hashed, user['id']))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Password updated successfully!")
        return redirect(url_for("index"))

    cursor.close()
    conn.close()
    return render_template("change_password.html", error=None)


# ---------------- BOOK LIBRARY ----------------
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

    return render_template("book_library.html",
                           title="Book Library",
                           books=books,
                           page=page,
                           total_pages=total_pages,
                           search=search)


# ---------------- USER REQUESTS ----------------
@app.route("/requests")
def requests():
    if not session.get("username"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM requests ORDER BY id ASC")
    all_requests = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("requests.html",
                           title="Book Requests",
                           all_requests=all_requests,
                           total_requests=len(all_requests))


# ADD REQUEST
@app.route("/add_request", methods=["GET", "POST"])
def add_request():
    if not session.get("username"):
        return redirect(url_for("login"))

    if request.method == "POST":
        book_name = request.form.get("book_name")
        author_name = request.form.get("author_name")
        info = request.form.get("additional_info")
        account = session.get("username")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO requests (book_name, author_name, additional_info, account)
            VALUES (%s, %s, %s, %s)
        """, (book_name, author_name, info, account))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("requests"))

    return render_template("add_request.html")


# MANAGE REQUESTS (Admin)
@app.route("/manage_requests")
def manage_requests():
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM requests ORDER BY id ASC")
    requests_list = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("manage_requests.html",
                           title="Manage Requests",
                           all_requests=requests_list,
                           total_requests=len(requests_list))


@app.route("/delete_request/<int:request_id>")
def delete_request(request_id):
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM requests WHERE id = %s", (request_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("manage_requests"))


# ---------------- MANAGE WEBSITE ----------------
@app.route("/manage_website")
def manage_website():
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))
    return render_template("manage_website.html")


# ---------------- ADD BOOK ----------------
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if session.get("role") not in ["admin", "superAdmin"]:
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

    return render_template("add_book.html")


# ---------------- EDIT BOOKS ----------------
@app.route("/edit_books", methods=["GET", "POST"])
def edit_books():
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        book_id = request.form.get("book_id")
        name = request.form.get("book_name")
        author = request.form.get("author_name")
        content = request.form.get("content")

        cursor.execute("""
            UPDATE books
            SET book_name = %s, author_name = %s, content = %s
            WHERE id = %s
        """, (name, author, content, book_id))
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

    return render_template("edit_books.html", books=books, search=search)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
