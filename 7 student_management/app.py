from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "student.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            course TEXT NOT NULL,
            email TEXT NOT NULL,
            attendance INTEGER NOT NULL
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    if count == 0:

        students = [
            ("Rahul Kumar", "101", "BCA",
             "rahul@gmail.com", 85),

            ("Amit Sharma", "102", "BCA",
             "amit@gmail.com", 78),

            ("Anil Nai", "103", "MCA",
             "anil@gmail.com", 92),

            ("Priya Verma", "104", "BCA",
             "priya@gmail.com", 88),

            ("Rohit Sahu", "105", "MCA",
             "rohit@gmail.com", 74)
        ]

        conn.executemany("""
            INSERT INTO students
            (name, roll_no, course, email, attendance)
            VALUES (?, ?, ?, ?, ?)
        """, students)

    conn.commit()
    conn.close()


@app.route("/")
def home():

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()

    total = len(students)

    if total > 0:
        average = round(
            sum(s["attendance"] for s in students)
            / total,
            1
        )
    else:
        average = 0

    eligible = sum(
        1 for s in students
        if s["attendance"] >= 75
    )

    conn.close()

    return render_template(
        "index.html",
        students=students,
        total=total,
        average=average,
        eligible=eligible
    )


@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"]
    roll_no = request.form["roll_no"]
    course = request.form["course"]
    email = request.form["email"]
    attendance = request.form["attendance"]

    conn = get_db()

    try:

        conn.execute("""
            INSERT INTO students
            (name, roll_no, course, email, attendance)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            roll_no,
            course,
            email,
            attendance
        ))

        conn.commit()

    except sqlite3.IntegrityError:

        conn.close()

        return """
        <h2>Roll Number already exists!</h2>
        <a href="/">Go Back</a>
        """

    conn.close()

    return redirect("/")


@app.route("/delete/<int:student_id>")
def delete_student(student_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":

    create_database()

    app.run(debug=True)