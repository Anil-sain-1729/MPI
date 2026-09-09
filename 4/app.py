from flask import Flask, request, redirect, url_for, session, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import random

app = Flask(__name__)
app.secret_key = "bookconnect-secret-key"

DATABASE = "bookconnect.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            bank_details TEXT,
            pan TEXT,
            status TEXT DEFAULT 'Active',
            created_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            writer_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            language TEXT,
            keywords TEXT,
            book_type TEXT,
            paper_type TEXT,
            size TEXT,
            cover_type TEXT,
            pages INTEGER,
            price REAL,
            isbn TEXT,
            status TEXT DEFAULT 'Published',
            created_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            reader_id INTEGER,
            printer_id INTEGER,
            delivery_id INTEGER,
            address TEXT,
            payment_method TEXT,
            status TEXT DEFAULT 'Placed',
            otp TEXT,
            created_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            book_id INTEGER,
            reader_id INTEGER,
            rating INTEGER,
            review TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# DESIGN
# =========================================================

STYLE = """
<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    background: #f7f2ea;
    color: #30221d;
}

nav {
    background: #5b1730;
    color: white;
    padding: 18px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 27px;
    font-weight: bold;
}

nav a {
    color: white;
    text-decoration: none;
    margin-left: 20px;
}

.hero {
    min-height: 430px;
    background: linear-gradient(135deg, #5b1730, #9d4059);
    color: white;
    padding: 80px 8%;
    display: flex;
    align-items: center;
}

.hero h1 {
    font-size: 55px;
    margin-bottom: 20px;
}

.hero p {
    font-size: 20px;
    max-width: 650px;
    line-height: 1.6;
}

.btn {
    display: inline-block;
    background: #f3c76b;
    color: #3a201d;
    padding: 13px 25px;
    border-radius: 8px;
    border: none;
    text-decoration: none;
    cursor: pointer;
    font-weight: bold;
    margin-top: 20px;
}

.container {
    width: 86%;
    max-width: 1200px;
    margin: 50px auto;
}

.title {
    text-align: center;
    font-size: 35px;
    margin-bottom: 35px;
}

.cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.card {
    background: white;
    padding: 30px 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(0,0,0,.08);
}

.card .icon {
    font-size: 50px;
    margin-bottom: 15px;
}

.card h3 {
    color: #5b1730;
    margin-bottom: 10px;
}

.card p {
    line-height: 1.5;
    color: #666;
}

.form-box {
    background: white;
    max-width: 700px;
    margin: 40px auto;
    padding: 35px;
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0,0,0,.1);
}

.form-box h2 {
    color: #5b1730;
    margin-bottom: 25px;
}

input, select, textarea {
    width: 100%;
    padding: 13px;
    margin: 8px 0 16px;
    border: 1px solid #ddd;
    border-radius: 7px;
    font-size: 15px;
}

textarea {
    min-height: 100px;
}

button {
    background: #5b1730;
    color: white;
    padding: 13px 22px;
    border: none;
    border-radius: 7px;
    cursor: pointer;
}

button:hover {
    opacity: .9;
}

.alert {
    padding: 15px;
    background: #fff0c9;
    border-radius: 8px;
    margin-bottom: 20px;
}

.book-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
}

.book {
    background: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 5px 18px rgba(0,0,0,.08);
}

.book-cover {
    height: 180px;
    background: linear-gradient(135deg, #5b1730, #c66c83);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 15px;
    font-size: 24px;
    font-weight: bold;
    padding: 15px;
}

.book h3 {
    margin-bottom: 8px;
}

.price {
    color: #8b2444;
    font-size: 21px;
    font-weight: bold;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

th, td {
    padding: 13px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}

th {
    background: #5b1730;
    color: white;
}

footer {
    background: #35121e;
    color: white;
    text-align: center;
    padding: 30px;
    margin-top: 70px;
}

@media(max-width: 800px) {
    .cards,
    .book-grid {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        font-size: 40px;
    }

    nav {
        flex-direction: column;
        gap: 15px;
    }
}

</style>
"""


# =========================================================
# NAVBAR
# =========================================================

def navbar():
    if "user_id" in session:
        return f"""
        <nav>
            <div class="logo">📚 BookConnect</div>
            <div>
                <a href="/dashboard">Dashboard</a>
                <a href="/books">Books</a>
                <a href="/logout">Logout</a>
            </div>
        </nav>
        """
    else:
        return """
        <nav>
            <div class="logo">📚 BookConnect</div>
            <div>
                <a href="/">Home</a>
                <a href="/books">Books</a>
                <a href="/login">Login</a>
            </div>
        </nav>
        """


def page(content, title="BookConnect"):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {STYLE}
    </head>
    <body>
        {navbar()}
        {content}
        <footer>
            <h3>📚 BookConnect</h3>
            <p>Connecting Writers, Printers, Delivery Partners and Readers.</p>
        </footer>
    </body>
    </html>
    """


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    content = """
    <section class="hero">
        <div>
            <h1>Books Connect People.</h1>
            <p>
                BookConnect is an online platform that connects
                writers, printers, delivery partners and readers
                in one simple system.
            </p>

            <a class="btn" href="#roles">Get Started</a>
        </div>
    </section>

    <div class="container" id="roles">

        <h2 class="title">Choose Your Role</h2>

        <div class="cards">

            <div class="card">
                <div class="icon">✍️</div>
                <h3>Writer</h3>
                <p>
                    Publish your book, select printing options
                    and reach readers.
                </p>
                <a class="btn" href="/register/writer">Join as Writer</a>
            </div>

            <div class="card">
                <div class="icon">🖨️</div>
                <h3>Printer</h3>
                <p>
                    Receive book printing orders and earn
                    through quality printing.
                </p>
                <a class="btn" href="/register/printer">Join as Printer</a>
            </div>

            <div class="card">
                <div class="icon">🚚</div>
                <h3>Delivery Boy</h3>
                <p>
                    Pick up books from printers and deliver
                    them to readers.
                </p>
                <a class="btn" href="/register/delivery">Join as Delivery</a>
            </div>

            <div class="card">
                <div class="icon">📖</div>
                <h3>Reader</h3>
                <p>
                    Search books, buy books, track orders
                    and give reviews.
                </p>
                <a class="btn" href="/register/reader">Join as Reader</a>
            </div>

        </div>
    </div>

    <div class="container">

        <h2 class="title">How BookConnect Works</h2>

        <div class="cards">

            <div class="card">
                <div class="icon">1️⃣</div>
                <h3>Writer Publishes</h3>
                <p>Writer uploads and publishes a book.</p>
            </div>

            <div class="card">
                <div class="icon">2️⃣</div>
                <h3>Printer Prints</h3>
                <p>Printer prints the ordered book.</p>
            </div>

            <div class="card">
                <div class="icon">3️⃣</div>
                <h3>Delivery</h3>
                <p>Delivery partner picks up and delivers.</p>
            </div>

            <div class="card">
                <div class="icon">4️⃣</div>
                <h3>Reader Reviews</h3>
                <p>Reader receives and reviews the book.</p>
            </div>

        </div>

    </div>
    """

    return page(content)


# =========================================================
# REGISTER
# =========================================================

@app.route("/register/<role>", methods=["GET", "POST"])
def register(role):

    roles = {
        "writer": "Writer",
        "printer": "Printer",
        "reader": "Reader",
        "delivery": "Delivery Boy"
    }

    if role not in roles:
        return redirect("/")

    if request.method == "POST":

        username = request.form["username"]
        name = request.form["name"]
        phone = request.form.get("phone", "")
        email = request.form.get("email", "")
        address = request.form.get("address", "")
        password = request.form["password"]

        bank = request.form.get("bank", "")
        pan = request.form.get("pan", "")

        if role == "writer":
            extra = bank
        else:
            extra = ""

        try:

            conn = get_db()

            conn.execute("""
                INSERT INTO users
                (username,name,phone,email,address,password,role,
                 bank_details,pan,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                username,
                name,
                phone,
                email,
                address,
                generate_password_hash(password),
                role,
                extra,
                pan,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:

            error = """
            <div class="alert">
                Username already exists. Please choose another username.
            </div>
            """

    else:
        error = ""

    extra_fields = ""

    if role == "writer":
        extra_fields = """
        <label>Bank Details</label>
        <input name="bank" placeholder="Bank account details">

        <label>PAN Number</label>
        <input name="pan" placeholder="PAN Number">
        """

    elif role == "reader":
        extra_fields = """
        <label>PAN Number</label>
        <input name="pan" placeholder="PAN Number">
        """

    elif role == "delivery":
        extra_fields = """
        <label>Driving Licence / Vehicle Documents</label>
        <input type="text" name="pan"
               placeholder="Document verification details">
        """

    content = f"""
    <div class="form-box">

        <h2>Create {roles[role]} ID</h2>

        {error}

        <form method="POST">

            <label>Username *</label>
            <input name="username" required>

            <label>Name *</label>
            <input name="name" required>

            <label>Phone Number</label>
            <input name="phone">

            <label>Email</label>
            <input type="email" name="email">

            <label>Address</label>
            <textarea name="address"></textarea>

            {extra_fields}

            <label>Password *</label>
            <input type="password" name="password" required>

            <button type="submit">
                Create {roles[role]} ID
            </button>

        </form>

        <p style="margin-top:20px">
            Already have an account?
            <a href="/login">Login</a>
        </p>

    </div>
    """

    return page(content, "Register - BookConnect")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["name"] = user["name"]

            return redirect("/dashboard")

        error = """
        <div class="alert">
            Invalid username or password.
        </div>
        """

    content = f"""
    <div class="form-box">

        <h2>Login to BookConnect</h2>

        {error}

        <form method="POST">

            <label>Username</label>
            <input name="username" required>

            <label>Password</label>
            <input type="password" name="password" required>

            <button type="submit">Login</button>

        </form>

    </div>
    """

    return page(content, "Login")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    role = session["role"]

    if role == "writer":
        return writer_dashboard()

    if role == "printer":
        return printer_dashboard()

    if role == "delivery":
        return delivery_dashboard()

    if role == "reader":
        return reader_dashboard()

    return redirect("/")


# =========================================================
# WRITER DASHBOARD
# =========================================================

def writer_dashboard():

    conn = get_db()

    books = conn.execute("""
        SELECT * FROM books
        WHERE writer_id=?
        ORDER BY id DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    book_html = ""

    for book in books:

        isbn = book["isbn"] if book["isbn"] else "Pending"

        book_html += f"""
        <div class="book">

            <div class="book-cover">
                {book["title"]}
            </div>

            <h3>{book["title"]}</h3>

            <p>{book["description"]}</p>

            <br>

            <p>
                Language: {book["language"]}<br>
                Type: {book["book_type"]}<br>
                Pages: {book["pages"]}<br>
                ISBN: {isbn}
            </p>

            <p class="price">
                ₹{book["price"]}
            </p>

        </div>
        """

    if not book_html:
        book_html = """
        <div class="alert">
            You have not published any books yet.
        </div>
        """

    content = f"""
    <div class="container">

        <h1>Welcome, {session["name"]} 👋</h1>

        <br>

        <a class="btn" href="/publish">
            + Publish New Book
        </a>

        <br><br>

        <h2>Your Books</h2>

        <br>

        <div class="book-grid">
            {book_html}
        </div>

    </div>
    """

    return page(content, "Writer Dashboard")


# =========================================================
# PUBLISH BOOK
# =========================================================

@app.route("/publish", methods=["GET", "POST"])
def publish():

    if "user_id" not in session or session["role"] != "writer":
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        language = request.form["language"]
        keywords = request.form["keywords"]
        book_type = request.form["book_type"]
        paper_type = request.form.get("paper_type", "")
        size = request.form.get("size", "")
        cover_type = request.form.get("cover_type", "")
        pages = int(request.form.get("pages", 0))
        price = float(request.form.get("price", 0))

        isbn = "BC-" + str(random.randint(100000, 999999))

        conn = get_db()

        conn.execute("""
            INSERT INTO books
            (writer_id,title,description,language,keywords,
             book_type,paper_type,size,cover_type,pages,
             price,isbn,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            session["user_id"],
            title,
            description,
            language,
            keywords,
            book_type,
            paper_type,
            size,
            cover_type,
            pages,
            price,
            isbn,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    content = """
    <div class="form-box">

        <h2>📚 Publish Your Book</h2>

        <form method="POST">

            <label>Book Title *</label>
            <input name="title" required>

            <label>Description</label>
            <textarea name="description"></textarea>

            <label>Language</label>
            <select name="language">
                <option>English</option>
                <option>Hindi</option>
                <option>Hinglish</option>
                <option>Other</option>
            </select>

            <label>Keywords</label>
            <input name="keywords"
                   placeholder="love, story, novel, motivation">

            <label>Publishing Type</label>
            <select name="book_type">
                <option>eBook</option>
                <option>Paperback</option>
                <option>Hardcover</option>
            </select>

            <label>Paper Type</label>
            <select name="paper_type">
                <option>Black & White</option>
                <option>Color</option>
            </select>

            <label>Paper Size</label>
            <select name="size">
                <option>5 × 8</option>
                <option>6 × 9</option>
                <option>8 × 12</option>
            </select>

            <label>Cover</label>
            <select name="cover_type">
                <option>Writer's Own Cover</option>
                <option>BookConnect Cover</option>
            </select>

            <label>Number of Pages</label>
            <input type="number" name="pages" min="1" required>

            <label>Book Price ₹</label>
            <input type="number" name="price"
                   min="1" step="0.01" required>

            <button type="submit">
                Publish Book
            </button>

        </form>

    </div>
    """

    return page(content, "Publish Book")


# =========================================================
# ALL BOOKS
# =========================================================

@app.route("/books")
def books():

    search = request.args.get("search", "")

    conn = get_db()

    if search:

        rows = conn.execute("""
            SELECT * FROM books
            WHERE title LIKE ?
               OR keywords LIKE ?
               OR description LIKE ?
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        )).fetchall()

    else:

        rows = conn.execute("""
            SELECT * FROM books
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    book_html = ""

    for book in rows:

        buy_button = ""

        if session.get("role") == "reader":

            buy_button = f"""
            <a class="btn" href="/buy/{book["id"]}">
                Buy Now
            </a>
            """

        book_html += f"""
        <div class="book">

            <div class="book-cover">
                {book["title"]}
            </div>

            <h3>{book["title"]}</h3>

            <p>{book["description"]}</p>

            <br>

            <p>
                Language: {book["language"]}<br>
                Type: {book["book_type"]}<br>
                Size: {book["size"]}
            </p>

            <br>

            <p class="price">
                ₹{book["price"]}
            </p>

            {buy_button}

        </div>
        """

    content = f"""
    <div class="container">

        <h1 class="title">📚 Explore Books</h1>

        <form method="GET">
            <input
                name="search"
                placeholder="Search by title, keyword..."
                value="{search}"
            >
            <button type="submit">Search</button>
        </form>

        <br><br>

        <div class="book-grid">
            {book_html}
        </div>

    </div>
    """

    return page(content, "Books")


# =========================================================
# BUY BOOK
# =========================================================

@app.route("/buy/<int:book_id>", methods=["GET", "POST"])
def buy(book_id):

    if "user_id" not in session or session["role"] != "reader":
        return redirect("/login")

    conn = get_db()

    book = conn.execute(
        "SELECT * FROM books WHERE id=?",
        (book_id,)
    ).fetchone()

    conn.close()

    if not book:
        return redirect("/books")

    if request.method == "POST":

        address = request.form["address"]
        payment = request.form["payment"]

        otp = str(random.randint(1000, 9999))

        conn = get_db()

        conn.execute("""
            INSERT INTO orders
            (book_id,reader_id,address,payment_method,
             status,otp,created_at)
            VALUES (?,?,?,?,?,?,?)
        """, (
            book_id,
            session["user_id"],
            address,
            payment,
            "Placed",
            otp,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

        conn.commit()
        conn.close()

        return redirect("/my-orders")

    content = f"""
    <div class="form-box">

        <h2>Buy: {book["title"]}</h2>

        <p>{book["description"]}</p>

        <br>

        <h3>Price: ₹{book["price"]}</h3>

        <form method="POST">

            <label>Delivery Address</label>
            <textarea name="address" required></textarea>

            <label>Payment Method</label>

            <select name="payment">
                <option>Cash on Delivery</option>
                <option>Online Payment</option>
            </select>

            <button type="submit">
                Place Order
            </button>

        </form>

    </div>
    """

    return page(content, "Buy Book")


# =========================================================
# READER DASHBOARD
# =========================================================

def reader_dashboard():

    conn = get_db()

    orders = conn.execute("""
        SELECT orders.*, books.title, books.price
        FROM orders
        JOIN books ON books.id = orders.book_id
        WHERE orders.reader_id=?
        ORDER BY orders.id DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    rows = ""

    for order in orders:

        rows += f"""
        <tr>
            <td>{order["id"]}</td>
            <td>{order["title"]}</td>
            <td>₹{order["price"]}</td>
            <td>{order["status"]}</td>
            <td>
                <a href="/review/{order["id"]}">
                    Review
                </a>
            </td>
        </tr>
        """

    content = f"""
    <div class="container">

        <h1>Reader Dashboard 📖</h1>

        <br>

        <a class="btn" href="/books">
            Search Books
        </a>

        <br><br>

        <h2>My Orders</h2>

        <br>

        <table>

            <tr>
                <th>Order</th>
                <th>Book</th>
                <th>Price</th>
                <th>Status</th>
                <th>Review</th>
            </tr>

            {rows}

        </table>

    </div>
    """

    return page(content, "Reader Dashboard")


# =========================================================
# MY ORDERS
# =========================================================

@app.route("/my-orders")
def my_orders():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    orders = conn.execute("""
        SELECT orders.*, books.title, books.price
        FROM orders
        JOIN books ON books.id=orders.book_id
        WHERE reader_id=?
        ORDER BY orders.id DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    rows = ""

    for o in orders:

        rows += f"""
        <tr>
            <td>{o["id"]}</td>
            <td>{o["title"]}</td>
            <td>₹{o["price"]}</td>
            <td>{o["payment_method"]}</td>
            <td>{o["status"]}</td>
            <td>
                <a href="/review/{o["id"]}">
                    Give Review
                </a>
            </td>
        </tr>
        """

    content = f"""
    <div class="container">

        <h1>📦 My Orders</h1>

        <br>

        <table>

            <tr>
                <th>Order ID</th>
                <th>Book</th>
                <th>Price</th>
                <th>Payment</th>
                <th>Status</th>
                <th>Review</th>
            </tr>

            {rows}

        </table>

    </div>
    """

    return page(content, "My Orders")


# =========================================================
# PRINTER DASHBOARD
# =========================================================

def printer_dashboard():

    conn = get_db()

    orders = conn.execute("""
        SELECT orders.*, books.title
        FROM orders
        JOIN books ON books.id=orders.book_id
        WHERE orders.printer_id IS NULL
        ORDER BY orders.id
    """).fetchall()

    my_orders = conn.execute("""
        SELECT orders.*, books.title
        FROM orders
        JOIN books ON books.id=orders.book_id
        WHERE orders.printer_id=?
        ORDER BY orders.id DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    available = ""

    for o in orders:

        available += f"""
        <div class="book">

            <h3>{o["title"]}</h3>

            <p>Order ID: {o["id"]}</p>

            <a class="btn"
               href="/printer/accept/{o["id"]}">
               Accept Order
            </a>

        </div>
        """

    current = ""

    for o in my_orders:

        current += f"""
        <tr>
            <td>{o["id"]}</td>
            <td>{o["title"]}</td>
            <td>{o["status"]}</td>
            <td>
                <a href="/printer/complete/{o["id"]}">
                    Mark Printed
                </a>
            </td>
        </tr>
        """

    content = f"""
    <div class="container">

        <h1>Printer Dashboard 🖨️</h1>

        <br>

        <h2>Available Orders</h2>

        <br>

        <div class="book-grid">
            {available}
        </div>

        <br><br>

        <h2>My Orders</h2>

        <br>

        <table>

            <tr>
                <th>Order</th>
                <th>Book</th>
                <th>Status</th>
                <th>Action</th>
            </tr>

            {current}

        </table>

    </div>
    """

    return page(content, "Printer Dashboard")


# =========================================================
# PRINTER ACCEPT
# =========================================================

@app.route("/printer/accept/<int:order_id>")
def printer_accept(order_id):

    if session.get("role") != "printer":
        return redirect("/login")

    conn = get_db()

    conn.execute("""
        UPDATE orders
        SET printer_id=?, status='Printing'
        WHERE id=? AND printer_id IS NULL
    """, (
        session["user_id"],
        order_id
    ))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# =========================================================
# PRINTER COMPLETE
# =========================================================

@app.route("/printer/complete/<int:order_id>")
def printer_complete(order_id):

    if session.get("role") != "printer":
        return redirect("/login")

    conn = get_db()

    conn.execute("""
        UPDATE orders
        SET status='Ready for Delivery'
        WHERE id=? AND printer_id=?
    """, (
        order_id,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# =========================================================
# DELIVERY DASHBOARD
# =========================================================

def delivery_dashboard():

    conn = get_db()

    orders = conn.execute("""
        SELECT orders.*, books.title
        FROM orders
        JOIN books ON books.id=orders.book_id
        WHERE orders.status='Ready for Delivery'
           OR orders.delivery_id=?
        ORDER BY orders.id DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    rows = ""

    for o in orders:

        action = ""

        if o["delivery_id"] is None:

            action = f"""
            <a class="btn"
               href="/delivery/accept/{o["id"]}">
               Accept
            </a>
            """

        elif o["status"] == "Out for Delivery":

            action = f"""
            <a class="btn"
               href="/delivery/deliver/{o["id"]}">
               Complete Delivery
            </a>
            """

        rows += f"""
        <tr>
            <td>{o["id"]}</td>
            <td>{o["title"]}</td>
            <td>{o["address"]}</td>
            <td>{o["status"]}</td>
            <td>{action}</td>
        </tr>
        """

    content = f"""
    <div class="container">

        <h1>Delivery Dashboard 🚚</h1>

        <br>

        <table>

            <tr>
                <th>Order</th>
                <th>Book</th>
                <th>Address</th>
                <th>Status</th>
                <th>Action</th>
            </tr>

            {rows}

        </table>

    </div>
    """

    return page(content, "Delivery Dashboard")


# =========================================================
# DELIVERY ACCEPT
# =========================================================

@app.route("/delivery/accept/<int:order_id>")
def delivery_accept(order_id):

    if session.get("role") != "delivery":
        return redirect("/login")

    conn = get_db()

    conn.execute("""
        UPDATE orders
        SET delivery_id=?, status='Out for Delivery'
        WHERE id=? AND delivery_id IS NULL
    """, (
        session["user_id"],
        order_id
    ))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# =========================================================
# DELIVERY COMPLETE
# =========================================================

@app.route("/delivery/deliver/<int:order_id>", methods=["GET", "POST"])
def delivery_complete(order_id):

    if session.get("role") != "delivery":
        return redirect("/login")

    conn = get_db()

    order = conn.execute("""
        SELECT * FROM orders
        WHERE id=? AND delivery_id=?
    """, (
        order_id,
        session["user_id"]
    )).fetchone()

    conn.close()

    if not order:
        return redirect("/dashboard")

    if request.method == "POST":

        entered_otp = request.form["otp"]

        if entered_otp == order["otp"]:

            conn = get_db()

            conn.execute("""
                UPDATE orders
                SET status='Delivered'
                WHERE id=?
            """, (order_id,))

            conn.commit()
            conn.close()

            return redirect("/dashboard")

        message = """
        <div class="alert">
            Incorrect OTP.
        </div>
        """

    else:
        message = ""

    content = f"""
    <div class="form-box">

        <h2>Complete Delivery</h2>

        {message}

        <p>
            Ask the reader for the delivery OTP.
        </p>

        <form method="POST">

            <label>Enter OTP</label>
            <input name="otp"
                   maxlength="4"
                   required>

            <button type="submit">
                Verify OTP
            </button>

        </form>

    </div>
    """

    return page(content, "Delivery Verification")


# =========================================================
# REVIEW
# =========================================================

@app.route("/review/<int:order_id>", methods=["GET", "POST"])
def review(order_id):

    if session.get("role") != "reader":
        return redirect("/login")

    conn = get_db()

    order = conn.execute("""
        SELECT orders.*, books.title
        FROM orders
        JOIN books ON books.id=orders.book_id
        WHERE orders.id=? AND orders.reader_id=?
    """, (
        order_id,
        session["user_id"]
    )).fetchone()

    conn.close()

    if not order:
        return redirect("/my-orders")

    if request.method == "POST":

        rating = int(request.form["rating"])
        review_text = request.form["review"]

        conn = get_db()

        conn.execute("""
            INSERT INTO reviews
            (order_id,book_id,reader_id,rating,review,created_at)
            VALUES (?,?,?,?,?,?)
        """, (
            order_id,
            order["book_id"],
            session["user_id"],
            rating,
            review_text,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

        conn.commit()
        conn.close()

        return redirect("/my-orders")

    content = f"""
    <div class="form-box">

        <h2>Review: {order["title"]}</h2>

        <form method="POST">

            <label>Rating</label>

            <select name="rating">
                <option value="5">⭐⭐⭐⭐⭐ 5</option>
                <option value="4">⭐⭐⭐⭐ 4</option>
                <option value="3">⭐⭐⭐ 3</option>
                <option value="2">⭐⭐ 2</option>
                <option value="1">⭐ 1</option>
            </select>

            <label>Your Review</label>

            <textarea name="review"
                      placeholder="Write your review..."
                      required></textarea>

            <button type="submit">
                Submit Review
            </button>

        </form>

    </div>
    """

    return page(content, "Review")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    init_db()

    print("---------------------------------------")
    print("       BOOKCONNECT STARTED")
    print("---------------------------------------")
    print("Open: http://127.0.0.1:5000")
    print("---------------------------------------")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )