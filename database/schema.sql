CREATE DATABASE IF NOT EXISTS student_system;

USE student_system;

-- =========================================
-- STUDENTS TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS students (
    roll_no INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    class_name VARCHAR(50)
);

-- =========================================
-- SUBJECTS TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS subjects (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(100) NOT NULL
);

-- =========================================
-- RESULTS TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS results (
    result_id INT PRIMARY KEY AUTO_INCREMENT,
    roll_no INT NOT NULL,
    subject_id INT NOT NULL,
    marks INT NOT NULL,

    FOREIGN KEY (roll_no)
        REFERENCES students(roll_no)
        ON DELETE CASCADE,

    FOREIGN KEY (subject_id)
        REFERENCES subjects(subject_id)
        ON DELETE CASCADE
);

-- =========================================
-- ATTENDANCE TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    roll_no INT NOT NULL,
    attendance_date DATE NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,

    FOREIGN KEY (roll_no)
        REFERENCES students(roll_no)
        ON DELETE CASCADE
);

-- =========================================
-- INSERT SUBJECTS
-- =========================================

INSERT INTO subjects (subject_name)
SELECT 'Data Structures'
WHERE NOT EXISTS (
    SELECT 1 FROM subjects WHERE subject_name = 'Data Structures'
);

INSERT INTO subjects (subject_name)
SELECT 'Python'
WHERE NOT EXISTS (
    SELECT 1 FROM subjects WHERE subject_name = 'Python'
);

INSERT INTO subjects (subject_name)
SELECT 'DBMS'
WHERE NOT EXISTS (
    SELECT 1 FROM subjects WHERE subject_name = 'DBMS'
);

INSERT INTO subjects (subject_name)
SELECT 'Mathematics'
WHERE NOT EXISTS (
    SELECT 1 FROM subjects WHERE subject_name = 'Mathematics'
);

INSERT INTO subjects (subject_name)
SELECT 'Computer Networks'
WHERE NOT EXISTS (
    SELECT 1 FROM subjects WHERE subject_name = 'Computer Networks'
);


-- =========================================
-- SAMPLE STUDENTS
-- =========================================

INSERT INTO students (roll_no, name, email, class_name)
VALUES
(101, 'Rahul Sharma', 'rahul@gmail.com', 'BT-12'),
(102, 'Aman Kumar', 'aman@gmail.com', 'BT-12'),
(103, 'Mohd Umar', 'umar@gmail.com', 'BT-12'),
(104, 'Arjun Singh', 'arjun@gmail.com', 'BT-12')
ON DUPLICATE KEY UPDATE roll_no = roll_no;


-- =========================================
-- SAMPLE RESULTS
-- =========================================

INSERT INTO results (roll_no, subject_id, marks)
SELECT 101, subject_id, 85
FROM subjects
WHERE subject_name = 'Data Structures';

INSERT INTO results (roll_no, subject_id, marks)
SELECT 101, subject_id, 78
FROM subjects
WHERE subject_name = 'Python';

INSERT INTO results (roll_no, subject_id, marks)
SELECT 101, subject_id, 91
FROM subjects
WHERE subject_name = 'DBMS';

INSERT INTO results (roll_no, subject_id, marks)
SELECT 102, subject_id, 92
FROM subjects
WHERE subject_name = 'Data Structures';

INSERT INTO results (roll_no, subject_id, marks)
SELECT 102, subject_id, 88
FROM subjects
WHERE subject_name = 'Python';

INSERT INTO results (roll_no, subject_id, marks)
SELECT 103, subject_id, 95
FROM subjects
WHERE subject_name = 'Data Structures';

INSERT INTO results (roll_no, subject_id, marks)
SELECT 103, subject_id, 89
FROM subjects
WHERE subject_name = 'Python';

INSERT INTO results (roll_no, subject_id, marks)
SELECT 103, subject_id, 94
FROM subjects
WHERE subject_name = 'DBMS';

INSERT INTO results (roll_no, subject_id, marks)
SELECT 104, subject_id, 75
FROM subjects
WHERE subject_name = 'Data Structures';

INSERT INTO results (roll_no, subject_id, marks)
SELECT 104, subject_id, 82
FROM subjects
WHERE subject_name = 'Python';