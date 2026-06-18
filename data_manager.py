import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "school.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '男',
            class_name TEXT NOT NULL,
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            address TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id TEXT NOT NULL,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '男',
            subject TEXT NOT NULL,
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            teacher_id INTEGER,
            schedule TEXT DEFAULT '',
            classroom TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            score REAL NOT NULL,
            exam_type TEXT DEFAULT '期中',
            semester TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT DEFAULT '出勤',
            remark TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
    """)
    conn.commit()
    conn.close()

class StudentManager:
    @staticmethod
    def get_all():
        conn = get_db()
        rows = conn.execute("SELECT * FROM students ORDER BY id").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(student_id):
        conn = get_db()
        row = conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def add(student):
        conn = get_db()
        c = conn.cursor()
        c.execute("""INSERT INTO students (student_id, name, gender, class_name, phone, email, address)
                     VALUES (?,?,?,?,?,?,?)""",
                  (student["student_id"], student["name"], student["gender"],
                   student["class_name"], student.get("phone",""),
                   student.get("email",""), student.get("address","")))
        conn.commit()
        new_id = c.lastrowid
        conn.close()
        return StudentManager.get_by_id(new_id)

    @staticmethod
    def update(student_id, updates):
        conn = get_db()
        conn.execute("""UPDATE students SET student_id=?, name=?, gender=?, class_name=?, phone=?, email=?, address=?
                        WHERE id=?""",
                     (updates["student_id"], updates["name"], updates["gender"],
                      updates["class_name"], updates.get("phone",""),
                      updates.get("email",""), updates.get("address",""), student_id))
        conn.commit()
        conn.close()
        return StudentManager.get_by_id(student_id)

    @staticmethod
    def delete(student_id):
        conn = get_db()
        conn.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def search(keyword):
        conn = get_db()
        kw = f"%{keyword}%"
        rows = conn.execute(
            "SELECT * FROM students WHERE name LIKE ? OR student_id LIKE ? OR class_name LIKE ? ORDER BY id",
            (kw, kw, kw)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

class TeacherManager:
    @staticmethod
    def get_all():
        conn = get_db()
        rows = conn.execute("SELECT * FROM teachers ORDER BY id").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(teacher_id):
        conn = get_db()
        row = conn.execute("SELECT * FROM teachers WHERE id=?", (teacher_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def add(teacher):
        conn = get_db()
        c = conn.cursor()
        c.execute("""INSERT INTO teachers (teacher_id, name, gender, subject, phone, email)
                     VALUES (?,?,?,?,?,?)""",
                  (teacher["teacher_id"], teacher["name"], teacher["gender"],
                   teacher["subject"], teacher.get("phone",""), teacher.get("email","")))
        conn.commit()
        new_id = c.lastrowid
        conn.close()
        return TeacherManager.get_by_id(new_id)

    @staticmethod
    def update(teacher_id, updates):
        conn = get_db()
        conn.execute("""UPDATE teachers SET teacher_id=?, name=?, gender=?, subject=?, phone=?, email=?
                        WHERE id=?""",
                     (updates["teacher_id"], updates["name"], updates["gender"],
                      updates["subject"], updates.get("phone",""), updates.get("email",""), teacher_id))
        conn.commit()
        conn.close()
        return TeacherManager.get_by_id(teacher_id)

    @staticmethod
    def delete(teacher_id):
        conn = get_db()
        conn.execute("DELETE FROM teachers WHERE id=?", (teacher_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def search(keyword):
        conn = get_db()
        kw = f"%{keyword}%"
        rows = conn.execute(
            "SELECT * FROM teachers WHERE name LIKE ? OR subject LIKE ? ORDER BY id",
            (kw, kw)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

class CourseManager:
    @staticmethod
    def get_all():
        conn = get_db()
        rows = conn.execute("SELECT * FROM courses ORDER BY id").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(course_id):
        conn = get_db()
        row = conn.execute("SELECT * FROM courses WHERE id=?", (course_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def add(course):
        conn = get_db()
        c = conn.cursor()
        c.execute("""INSERT INTO courses (course_name, teacher_id, schedule, classroom)
                     VALUES (?,?,?,?)""",
                  (course["course_name"], course["teacher_id"],
                   course.get("schedule",""), course.get("classroom","")))
        conn.commit()
        new_id = c.lastrowid
        conn.close()
        return CourseManager.get_by_id(new_id)

    @staticmethod
    def update(course_id, updates):
        conn = get_db()
        conn.execute("""UPDATE courses SET course_name=?, teacher_id=?, schedule=?, classroom=?
                        WHERE id=?""",
                     (updates["course_name"], updates["teacher_id"],
                      updates.get("schedule",""), updates.get("classroom",""), course_id))
        conn.commit()
        conn.close()
        return CourseManager.get_by_id(course_id)

    @staticmethod
    def delete(course_id):
        conn = get_db()
        conn.execute("DELETE FROM courses WHERE id=?", (course_id,))
        conn.commit()
        conn.close()
        return True

class GradeManager:
    @staticmethod
    def get_all():
        conn = get_db()
        rows = conn.execute("SELECT * FROM grades ORDER BY id").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_student(student_id):
        conn = get_db()
        rows = conn.execute("SELECT * FROM grades WHERE student_id=?", (student_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_course(course_id):
        conn = get_db()
        rows = conn.execute("SELECT * FROM grades WHERE course_id=?", (course_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def add(grade):
        conn = get_db()
        c = conn.cursor()
        c.execute("""INSERT INTO grades (student_id, course_id, score, exam_type, semester)
                     VALUES (?,?,?,?,?)""",
                  (grade["student_id"], grade["course_id"], grade["score"],
                   grade.get("exam_type",""), grade.get("semester","")))
        conn.commit()
        new_id = c.lastrowid
        conn.close()
        return GradeManager.get_by_id(new_id)

    @staticmethod
    def get_by_id(grade_id):
        conn = get_db()
        row = conn.execute("SELECT * FROM grades WHERE id=?", (grade_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def delete(grade_id):
        conn = get_db()
        conn.execute("DELETE FROM grades WHERE id=?", (grade_id,))
        conn.commit()
        conn.close()
        return True

class AttendanceManager:
    @staticmethod
    def get_all():
        conn = get_db()
        rows = conn.execute("SELECT * FROM attendance ORDER BY id").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_student(student_id):
        conn = get_db()
        rows = conn.execute("SELECT * FROM attendance WHERE student_id=?", (student_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_date(date_str):
        conn = get_db()
        rows = conn.execute("SELECT * FROM attendance WHERE date=?", (date_str,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def add(record):
        conn = get_db()
        c = conn.cursor()
        c.execute("""INSERT INTO attendance (student_id, course_id, date, status, remark)
                     VALUES (?,?,?,?,?)""",
                  (record["student_id"], record["course_id"], record["date"],
                   record["status"], record.get("remark","")))
        conn.commit()
        new_id = c.lastrowid
        conn.close()
        return AttendanceManager.get_by_id(new_id)

    @staticmethod
    def get_by_id(attendance_id):
        conn = get_db()
        row = conn.execute("SELECT * FROM attendance WHERE id=?", (attendance_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def delete(attendance_id):
        conn = get_db()
        conn.execute("DELETE FROM attendance WHERE id=?", (attendance_id,))
        conn.commit()
        conn.close()
        return True

init_db()
