from flask import Flask, render_template, request, redirect, url_for

from db import get_connection

from dsa.sorting import merge_sort
from dsa.searching import binary_search


app = Flask(__name__)


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def index():

    return render_template("index.html")


# =========================================
# ADD STUDENT
# =========================================

@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        roll_no = request.form["roll_no"]
        name = request.form["name"]
        email = request.form["email"]
        class_name = request.form["class_name"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO students
        (roll_no, name, email, class_name)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (roll_no, name, email, class_name)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("students"))

    return render_template("add_student.html")


# =========================================
# DISPLAY STUDENTS
# =========================================

@app.route("/students")
def students():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY roll_no
    """)

    students_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "students.html",
        students=students_data
    )


# =========================================
# RESULTS
# =========================================

@app.route("/results", methods=["GET", "POST"])
def results():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        roll_no = request.form["roll_no"]
        subject_id = request.form["subject_id"]
        marks = request.form["marks"]

        cursor.execute("""
            INSERT INTO results
            (roll_no, subject_id, marks)
            VALUES (%s, %s, %s)
        """, (roll_no, subject_id, marks))

        connection.commit()

    # Get result records using JOIN

    cursor.execute("""
        SELECT
            s.roll_no,
            s.name,
            sub.subject_name,
            r.marks

        FROM students s

        JOIN results r
            ON s.roll_no = r.roll_no

        JOIN subjects sub
            ON r.subject_id = sub.subject_id

        ORDER BY s.roll_no
    """)

    results_data = cursor.fetchall()

    # Get students for dropdown

    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY roll_no
    """)

    students_data = cursor.fetchall()

    # Get subjects for dropdown

    cursor.execute("""
        SELECT *
        FROM subjects
        ORDER BY subject_id
    """)

    subjects_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "results.html",
        results=results_data,
        students=students_data,
        subjects=subjects_data
    )


# =========================================
# ATTENDANCE
# =========================================

@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        roll_no = request.form["roll_no"]
        attendance_date = request.form["attendance_date"]
        status = request.form["status"]

        cursor.execute("""
            INSERT INTO attendance
            (roll_no, attendance_date, status)
            VALUES (%s, %s, %s)
        """, (
            roll_no,
            attendance_date,
            status
        ))

        connection.commit()

    # Attendance summary using JOIN + aggregation

    cursor.execute("""
        SELECT
            s.roll_no,
            s.name,

            COUNT(a.attendance_id) AS total_days,

            SUM(
                CASE
                    WHEN a.status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS present_days,

            ROUND(
                (
                    SUM(
                        CASE
                            WHEN a.status = 'Present'
                            THEN 1
                            ELSE 0
                        END
                    ) / COUNT(a.attendance_id)
                ) * 100,
                2
            ) AS attendance_percentage

        FROM students s

        LEFT JOIN attendance a
            ON s.roll_no = a.roll_no

        GROUP BY s.roll_no, s.name
        ORDER BY s.roll_no
    """)

    attendance_data = cursor.fetchall()

    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY roll_no
    """)

    students_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "attendance.html",
        attendance=attendance_data,
        students=students_data
    )


# =========================================
# STUDENT RANKING
# =========================================

@app.route("/ranking")
def ranking():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # SQL aggregation

    cursor.execute("""
        SELECT
            s.roll_no,
            s.name,
            COALESCE(AVG(r.marks), 0) AS average

        FROM students s

        LEFT JOIN results r
            ON s.roll_no = r.roll_no

        GROUP BY s.roll_no, s.name

        ORDER BY s.roll_no
    """)

    students_data = cursor.fetchall()

    cursor.close()
    connection.close()

    # Convert average to float

    for student in students_data:
        student["average"] = float(student["average"])

    # =====================================
    # DSA: MERGE SORT
    # =====================================

    ranked_students = merge_sort(students_data)

    # Assign ranks

    for index, student in enumerate(ranked_students):

        student["rank"] = index + 1

    return render_template(
        "ranking.html",
        students=ranked_students
    )


# =========================================
# SEARCH STUDENT
# =========================================

@app.route("/search")
def search():

    roll_no = request.args.get("roll_no")

    if not roll_no:
        return redirect(url_for("students"))

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Get students sorted by roll number
    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY roll_no
    """)

    students_data = cursor.fetchall()

    cursor.close()
    connection.close()

    # =====================================
    # DSA: BINARY SEARCH
    # =====================================

    student = binary_search(
        students_data,
        int(roll_no)
    )

    return render_template(
        "students.html",
        students=[student] if student else [],
        search=True
    )


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":
    app.run(debug=True)