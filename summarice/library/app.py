import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from database import get_db_connection
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "randomizerz"

# ---------- FILE UPLOAD CONFIG ----------
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "book_images")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4 MB limit 


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file_storage):
    """Save uploaded file, return saved filename (unique)."""
    if not file_storage:
        return None
    filename = secure_filename(file_storage.filename)
    if filename == "" or not allowed_file(filename):
        return None

    ext = filename.rsplit(".", 1)[1].lower()
    new_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], new_name)
    file_storage.save(save_path)
    return new_name


def remove_image_file(filename):
    """Delete image file from disk if exists."""
    if not filename:
        return
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    try:
        if os.path.exists(path):
            os.remove(path)
    except:
        pass


# ---------- SERVE IMAGE FILES ----------
@app.route("/book_images/<filename>")
def book_images(filename):
    """Serve uploaded book images."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ---------------- HOME / ABOUT ----------------
@app.route("/")
def index():
    return render_template("index.html", title="Home")


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

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return render_template("signup.html", error="Username is already taken.")

        cursor.close()
        conn.close()

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        session["signup_data"] = {
            "fullname": fullname,
            "username": username,
            "password": password
        }

        return redirect(url_for("slider_verification"))

    return render_template("signup.html")


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
    cursor.execute(f"SELECT * FROM users ORDER BY {sort_by} {order}")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "manage_accounts.html",
        users=users,
        sort_by=sort_by,
        order=order
    )


@app.route("/delete_account/<int:user_id>")
def delete_account(user_id):
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    return_to = request.args.get("return_to", "manage_accounts")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Account deleted successfully!")
    return redirect(url_for(return_to))


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

        flash("Account updated successfully!")
        return redirect(url_for(return_to))

    cursor.close()
    conn.close()

    return render_template("edit_account.html", user=user, return_to=return_to)


@app.route("/reset_password/<int:user_id>")
def reset_password(user_id):
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    return_to = request.args.get("return_to", "manage_accounts")

    temp_password = "Summarice123"
    hashed = generate_password_hash(temp_password)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Temporary password set: {temp_password}")
    return redirect(url_for(return_to))


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
    cursor.execute(f"SELECT * FROM users ORDER BY {sort_by} {order}")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "advance_manage_accounts.html",
        users=users,
        sort_by=sort_by,
        order=order
    )


# ---------------- CHANGE PASSWORD ----------------
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))

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
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")
    page = int(request.args.get("page", 1))
    per_page = 3
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if sort == "author":
        sort_column = "author_name"
    else:
        sort_column = "book_name"

    order_sql = "ASC" if order == "asc" else "DESC"

    # Count books
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

    # Fetch books
    if search:
        cursor.execute(f"""
            SELECT * FROM books
            WHERE book_name LIKE %s OR author_name LIKE %s
            ORDER BY {sort_column} {order_sql}
            LIMIT %s OFFSET %s
        """, (f"%{search}%", f"%{search}%", per_page, offset))
    else:
        cursor.execute(f"""
            SELECT * FROM books
            ORDER BY {sort_column} {order_sql}
            LIMIT %s OFFSET %s
        """, (per_page, offset))

    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "book_library.html",
        books=books,
        page=page,
        total_pages=total_pages,
        search=search,
        sort=sort,
        order=order
    )


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

@app.route("/delete_request/<int:request_id>")
def delete_request(request_id):
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT account FROM requests WHERE id = %s", (request_id,))
    owner = cursor.fetchone()

    if not owner or owner["account"] != username:
        flash("You cannot delete this request.")
        return redirect(url_for("requests"))

    cursor.execute("DELETE FROM requests WHERE id = %s", (request_id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Request deleted.")
    return redirect(url_for("requests"))


# ---------------- MANAGE REQUESTS ----------------
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


@app.route("/admin_delete_request/<int:request_id>")
def admin_delete_request(request_id):
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
        file = request.files.get("image")

        saved_filename = None
        if file and allowed_file(file.filename):
            saved_filename = save_uploaded_file(file)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (book_name, author_name, content, image_filename)
            VALUES (%s, %s, %s, %s)
        """, (book_name, author_name, content, saved_filename))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("books"))

    return render_template("add_book.html")


# ---------------- DELETE BOOK ----------------
@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT image_filename FROM books WHERE id = %s", (book_id,))
    row = cursor.fetchone()

    if row and row.get("image_filename"):
        remove_image_file(row["image_filename"])

    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Book deleted.")
    return redirect(url_for("edit_books"))


# ---------------- DELETE BOOK IMAGE ----------------
@app.route("/delete_book_image/<int:book_id>")
def delete_book_image(book_id):
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT image_filename FROM books WHERE id = %s", (book_id,))
    row = cursor.fetchone()

    if row and row.get("image_filename"):
        remove_image_file(row["image_filename"])

    cursor.execute("UPDATE books SET image_filename = NULL WHERE id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Image removed.")
    return redirect(url_for("edit_books"))


# ---------------- EDIT BOOKS ----------------
@app.route("/edit_books", methods=["GET", "POST"])
def edit_books():
    if session.get("role") not in ["admin", "superAdmin"]:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # SAVE EDIT
    if request.method == "POST":
        book_id = request.form.get("book_id")
        name = request.form.get("book_name")
        author = request.form.get("author_name")
        content = request.form.get("content")
        file = request.files.get("image")

        cursor.execute("SELECT image_filename FROM books WHERE id = %s", (book_id,))
        row = cursor.fetchone()
        old_image = row["image_filename"] if row else None

        new_filename = old_image
        if file and allowed_file(file.filename):
            new_filename = save_uploaded_file(file)
            if old_image:
                remove_image_file(old_image)

        cursor.execute("""
            UPDATE books
            SET book_name = %s, author_name = %s, content = %s, image_filename = %s
            WHERE id = %s
        """, (name, author, content, new_filename, book_id))
        conn.commit()

    # FETCH LIST
    search = request.args.get("search", "").strip()
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")

    sort_column = "author_name" if sort == "author" else "book_name"
    order_sql = "ASC" if order == "asc" else "DESC"

    if search:
        cursor.execute(f"""
            SELECT * FROM books
            WHERE book_name LIKE %s OR author_name LIKE %s
            ORDER BY {sort_column} {order_sql}
        """, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute(f"SELECT * FROM books ORDER BY {sort_column} {order_sql}")

    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "edit_books.html",
        books=books,
        search=search,
        sort=sort,
        order=order
    )
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
