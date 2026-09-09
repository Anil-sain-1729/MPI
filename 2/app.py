from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.secret_key = "bookconnect_demo_secret_key"

DATABASE = "bookconnect.db"

UPLOAD_FOLDER = "uploads"

BOOK_FOLDER = os.path.join(
    UPLOAD_FOLDER,
    "books"
)

DOCUMENT_FOLDER = os.path.join(
    UPLOAD_FOLDER,
    "documents"
)

os.makedirs(BOOK_FOLDER, exist_ok=True)
os.makedirs(DOCUMENT_FOLDER, exist_ok=True)


# ---------------------------------------
# DATABASE
# ---------------------------------------

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def create_tables():

    conn = get_db()

    # Users

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            name TEXT NOT NULL,

            number TEXT NOT NULL,

            email TEXT,

            address TEXT,

            password TEXT NOT NULL,

            role TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # Writer details

    conn.execute("""
        CREATE TABLE IF NOT EXISTS writer_details (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            bank_details TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)


    # Delivery documents

    conn.execute("""
        CREATE TABLE IF NOT EXISTS delivery_documents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            driving_license TEXT,

            vehicle_rc TEXT,

            verification_status TEXT DEFAULT 'Pending',

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)


    # Books

    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            writer_id INTEGER,

            title TEXT NOT NULL,

            language TEXT,

            description TEXT,

            keywords TEXT,

            publish_type TEXT,

            paper_type TEXT,

            paper_size TEXT,

            cover_type TEXT,

            pdf_file TEXT,

            price REAL,

            isbn TEXT,

            status TEXT DEFAULT 'Processing',

            FOREIGN KEY(writer_id)
            REFERENCES users(id)

        )
    """)


    # Orders

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            reader_id INTEGER,

            book_id INTEGER,

            printer_id INTEGER,

            delivery_id INTEGER,

            address TEXT,

            payment_method TEXT,

            status TEXT DEFAULT 'Order Placed',

            otp TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(reader_id)
            REFERENCES users(id),

            FOREIGN KEY(book_id)
            REFERENCES books(id)

        )
    """)


    # Reviews

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            reader_id INTEGER,

            book_id INTEGER,

            rating INTEGER,

            review TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    conn.commit()

    conn.close()


# ---------------------------------------
# HOME
# ---------------------------------------

@app.route("/")
def index():

    conn = get_db()

    books = conn.execute("""
        SELECT
            books.*,
            users.name AS writer_name

        FROM books

        JOIN users
        ON books.writer_id = users.id

        WHERE books.status = 'Published'

        ORDER BY books.id DESC

    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        books=books
    )


# ---------------------------------------
# REGISTER
# ---------------------------------------

@app.route(
    "/register/<role>",
    methods=["GET", "POST"]
)
def register(role):

    allowed_roles = [
        "writer",
        "printer",
        "reader",
        "delivery"
    ]

    if role not in allowed_roles:

        return "Invalid role"


    if request.method == "POST":

        username = request.form["username"]

        name = request.form["name"]

        number = request.form["number"]

        email = request.form.get("email")

        address = request.form.get("address")

        password = request.form["password"]


        hashed_password = generate_password_hash(
            password
        )


        conn = get_db()

        try:

            cursor = conn.execute("""
                INSERT INTO users
                (
                    username,
                    name,
                    number,
                    email,
                    address,
                    password,
                    role
                )

                VALUES (?, ?, ?, ?, ?, ?, ?)

            """, (
                username,
                name,
                number,
                email,
                address,
                hashed_password,
                role
            ))


            user_id = cursor.lastrowid


            # Writer bank details

            if role == "writer":

                bank_details = request.form.get(
                    "bank_details"
                )

                conn.execute("""
                    INSERT INTO writer_details
                    (
                        user_id,
                        bank_details
                    )

                    VALUES (?, ?)

                """, (
                    user_id,
                    bank_details
                ))


            # Delivery documents

            if role == "delivery":

                license_file = request.files.get(
                    "driving_license"
                )

                rc_file = request.files.get(
                    "vehicle_rc"
                )


                license_name = ""

                rc_name = ""


                if license_file:

                    license_name = secure_filename(
                        license_file.filename
                    )

                    license_file.save(
                        os.path.join(
                            DOCUMENT_FOLDER,
                            license_name
                        )
                    )


                if rc_file:

                    rc_name = secure_filename(
                        rc_file.filename
                    )

                    rc_file.save(
                        os.path.join(
                            DOCUMENT_FOLDER,
                            rc_name
                        )
                    )


                conn.execute("""
                    INSERT INTO delivery_documents
                    (
                        user_id,
                        driving_license,
                        vehicle_rc
                    )

                    VALUES (?, ?, ?)

                """, (
                    user_id,
                    license_name,
                    rc_name
                ))


            conn.commit()

            flash(
                "Account created successfully!",
                "success"
            )

            return redirect(
                url_for(
                    "login"
                )
            )


        except sqlite3.IntegrityError:

            flash(
                "Username already exists.",
                "error"
            )


        finally:

            conn.close()


    return render_template(
        "register.html",
        role=role
    )


# ---------------------------------------
# LOGIN
# ---------------------------------------

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]


        conn = get_db()

        user = conn.execute("""
            SELECT *

            FROM users

            WHERE username = ?

        """, (
            username,
        )).fetchone()

        conn.close()


        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["username"] = user["username"]

            session["role"] = user["role"]

            return redirect(
                url_for(
                    "dashboard"
                )
            )


        flash(
            "Wrong username or password.",
            "error"
        )


    return render_template(
        "login.html"
    )


# ---------------------------------------
# DASHBOARD
# ---------------------------------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    conn = get_db()


    user = conn.execute("""
        SELECT *

        FROM users

        WHERE id = ?

    """, (
        session["user_id"],
    )).fetchone()


    books = []

    orders = []


    if user["role"] == "writer":

        books = conn.execute("""
            SELECT *

            FROM books

            WHERE writer_id = ?

            ORDER BY id DESC

        """, (
            user["id"],
        )).fetchall()


    elif user["role"] == "reader":

        orders = conn.execute("""
            SELECT
                orders.*,
                books.title

            FROM orders

            JOIN books
            ON orders.book_id = books.id

            WHERE orders.reader_id = ?

            ORDER BY orders.id DESC

        """, (
            user["id"],
        )).fetchall()


    elif user["role"] == "printer":

        orders = conn.execute("""
            SELECT
                orders.*,
                books.title

            FROM orders

            JOIN books
            ON orders.book_id = books.id

            ORDER BY orders.id DESC

        """).fetchall()


    elif user["role"] == "delivery":

        orders = conn.execute("""
            SELECT
                orders.*,
                books.title

            FROM orders

            JOIN books
            ON orders.book_id = books.id

            WHERE orders.delivery_id = ?

            ORDER BY orders.id DESC

        """, (
            user["id"],
        )).fetchall()


    conn.close()


    return render_template(
        "dashboard.html",
        user=user,
        books=books,
        orders=orders
    )


# ---------------------------------------
# PUBLISH BOOK
# ---------------------------------------

@app.route(
    "/publish-book",
    methods=["GET", "POST"]
)
def publish_book():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session["role"] != "writer":

        return "Only Writer can publish books."


    if request.method == "POST":

        title = request.form["title"]

        language = request.form["language"]

        description = request.form["description"]

        keywords = request.form["keywords"]

        publish_type = request.form["publish_type"]

        paper_type = request.form["paper_type"]

        paper_size = request.form["paper_size"]

        cover_type = request.form["cover_type"]

        price = request.form["price"]


        pdf = request.files.get(
            "pdf"
        )


        pdf_name = ""


        if pdf and pdf.filename:

            pdf_name = secure_filename(
                pdf.filename
            )

            pdf.save(
                os.path.join(
                    BOOK_FOLDER,
                    pdf_name
                )
            )


        conn = get_db()


        conn.execute("""
            INSERT INTO books
            (
                writer_id,
                title,
                language,
                description,
                keywords,
                publish_type,
                paper_type,
                paper_size,
                cover_type,
                pdf_file,
                price
            )

            VALUES
            (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?
            )

        """, (
            session["user_id"],
            title,
            language,
            description,
            keywords,
            publish_type,
            paper_type,
            paper_size,
            cover_type,
            pdf_name,
            price
        ))


        conn.commit()

        conn.close()


        flash(
            "Book submitted successfully!",
            "success"
        )


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "publish_book.html"
    )


# ---------------------------------------
# BUY BOOK
# ---------------------------------------

@app.route(
    "/buy/<int:book_id>",
    methods=["POST"]
)
def buy_book(book_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session["role"] != "reader":

        return "Only Reader can buy books."


    address = request.form["address"]

    payment = request.form["payment"]


    conn = get_db()


    book = conn.execute("""
        SELECT *

        FROM books

        WHERE id = ?

    """, (
        book_id,
    )).fetchone()


    if not book:

        conn.close()

        return "Book not found."


    conn.execute("""
        INSERT INTO orders
        (
            reader_id,
            book_id,
            address,
            payment_method
        )

        VALUES (?, ?, ?, ?)

    """, (
        session["user_id"],
        book_id,
        address,
        payment
    ))


    conn.commit()

    conn.close()


    flash(
        "Order placed successfully!",
        "success"
    )


    return redirect(
        url_for("dashboard")
    )


# ---------------------------------------
# PRINTER ACCEPT ORDER
# ---------------------------------------

@app.route(
    "/accept-order/<int:order_id>"
)
def accept_order(order_id):

    if session.get("role") != "printer":

        return "Only printer can accept orders."


    conn = get_db()


    conn.execute("""
        UPDATE orders

        SET
            printer_id = ?,
            status = 'Printing'

        WHERE id = ?

    """, (
        session["user_id"],
        order_id
    ))


    conn.commit()

    conn.close()


    return redirect(
        url_for("dashboard")
    )


# ---------------------------------------
# DELIVERY COMPLETE
# ---------------------------------------

@app.route(
    "/complete-delivery/<int:order_id>",
    methods=["POST"]
)
def complete_delivery(order_id):

    if session.get("role") != "delivery":

        return "Only delivery partner can complete delivery."


    otp = request.form["otp"]


    conn = get_db()


    order = conn.execute("""
        SELECT *

        FROM orders

        WHERE id = ?

    """, (
        order_id,
    )).fetchone()


    # Demo OTP

    if otp == "123456":

        conn.execute("""
            UPDATE orders

            SET
                delivery_id = ?,
                status = 'Delivered'

            WHERE id = ?

        """, (
            session["user_id"],
            order_id
        ))


        conn.commit()

        conn.close()


        return "Delivery completed successfully!"


    conn.close()


    return "Wrong OTP."


# ---------------------------------------
# REVIEW
# ---------------------------------------

@app.route(
    "/review/<int:book_id>",
    methods=["POST"]
)
def review(book_id):

    if session.get("role") != "reader":

        return "Only reader can review."


    rating = int(
        request.form["rating"]
    )

    review_text = request.form["review"]


    if rating < 1 or rating > 5:

        return "Rating must be between 1 and 5."


    conn = get_db()


    conn.execute("""
        INSERT INTO reviews
        (
            reader_id,
            book_id,
            rating,
            review
        )

        VALUES (?, ?, ?, ?)

    """, (
        session["user_id"],
        book_id,
        rating,
        review_text
    ))


    conn.commit()

    conn.close()


    return "Review submitted successfully!"


# ---------------------------------------
# LOGOUT
# ---------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("index")
    )


# ---------------------------------------
# START SERVER
# ---------------------------------------

if __name__ == "__main__":

    create_tables()

    app.run(
        debug=True
    )