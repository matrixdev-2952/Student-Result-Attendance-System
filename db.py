import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Um@r1234",
        database="student_system"
    )

    return connection