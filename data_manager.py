import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def ensure_data_file(filename, default_data):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    return path

def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_next_id(data):
    if not data:
        return 1
    return max(item["id"] for item in data) + 1

class StudentManager:
    FILE = "students.json"

    @staticmethod
    def get_all():
        return load_data(StudentManager.FILE)

    @staticmethod
    def get_by_id(student_id):
        data = load_data(StudentManager.FILE)
        for s in data:
            if s["id"] == student_id:
                return s
        return None

    @staticmethod
    def add(student):
        data = load_data(StudentManager.FILE)
        student["id"] = get_next_id(data)
        student["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.append(student)
        save_data(StudentManager.FILE, data)
        return student

    @staticmethod
    def update(student_id, updates):
        data = load_data(StudentManager.FILE)
        for s in data:
            if s["id"] == student_id:
                s.update(updates)
                save_data(StudentManager.FILE, data)
                return s
        return None

    @staticmethod
    def delete(student_id):
        data = load_data(StudentManager.FILE)
        new_data = [s for s in data if s["id"] != student_id]
        if len(new_data) != len(data):
            save_data(StudentManager.FILE, new_data)
            return True
        return False

    @staticmethod
    def search(keyword):
        data = load_data(StudentManager.FILE)
        keyword = keyword.lower()
        return [s for s in data if
                keyword in s["name"].lower() or
                keyword in s.get("student_id", "").lower() or
                keyword in s.get("class_name", "").lower()]

class TeacherManager:
    FILE = "teachers.json"

    @staticmethod
    def get_all():
        return load_data(TeacherManager.FILE)

    @staticmethod
    def get_by_id(teacher_id):
        data = load_data(TeacherManager.FILE)
        for t in data:
            if t["id"] == teacher_id:
                return t
        return None

    @staticmethod
    def add(teacher):
        data = load_data(TeacherManager.FILE)
        teacher["id"] = get_next_id(data)
        teacher["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.append(teacher)
        save_data(TeacherManager.FILE, data)
        return teacher

    @staticmethod
    def update(teacher_id, updates):
        data = load_data(TeacherManager.FILE)
        for t in data:
            if t["id"] == teacher_id:
                t.update(updates)
                save_data(TeacherManager.FILE, data)
                return t
        return None

    @staticmethod
    def delete(teacher_id):
        data = load_data(TeacherManager.FILE)
        new_data = [t for t in data if t["id"] != teacher_id]
        if len(new_data) != len(data):
            save_data(TeacherManager.FILE, new_data)
            return True
        return False

    @staticmethod
    def search(keyword):
        data = load_data(TeacherManager.FILE)
        keyword = keyword.lower()
        return [t for t in data if
                keyword in t["name"].lower() or
                keyword in t.get("subject", "").lower()]

class CourseManager:
    FILE = "courses.json"

    @staticmethod
    def get_all():
        return load_data(CourseManager.FILE)

    @staticmethod
    def get_by_id(course_id):
        data = load_data(CourseManager.FILE)
        for c in data:
            if c["id"] == course_id:
                return c
        return None

    @staticmethod
    def add(course):
        data = load_data(CourseManager.FILE)
        course["id"] = get_next_id(data)
        course["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.append(course)
        save_data(CourseManager.FILE, data)
        return course

    @staticmethod
    def update(course_id, updates):
        data = load_data(CourseManager.FILE)
        for c in data:
            if c["id"] == course_id:
                c.update(updates)
                save_data(CourseManager.FILE, data)
                return c
        return None

    @staticmethod
    def delete(course_id):
        data = load_data(CourseManager.FILE)
        new_data = [c for c in data if c["id"] != course_id]
        if len(new_data) != len(data):
            save_data(CourseManager.FILE, new_data)
            return True
        return False

class GradeManager:
    FILE = "grades.json"

    @staticmethod
    def get_all():
        return load_data(GradeManager.FILE)

    @staticmethod
    def get_by_student(student_id):
        data = load_data(GradeManager.FILE)
        return [g for g in data if g["student_id"] == student_id]

    @staticmethod
    def get_by_course(course_id):
        data = load_data(GradeManager.FILE)
        return [g for g in data if g["course_id"] == course_id]

    @staticmethod
    def add(grade):
        data = load_data(GradeManager.FILE)
        grade["id"] = get_next_id(data)
        grade["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.append(grade)
        save_data(GradeManager.FILE, data)
        return grade

    @staticmethod
    def delete(grade_id):
        data = load_data(GradeManager.FILE)
        new_data = [g for g in data if g["id"] != grade_id]
        if len(new_data) != len(data):
            save_data(GradeManager.FILE, new_data)
            return True
        return False

class AttendanceManager:
    FILE = "attendance.json"

    @staticmethod
    def get_all():
        return load_data(AttendanceManager.FILE)

    @staticmethod
    def get_by_student(student_id):
        data = load_data(AttendanceManager.FILE)
        return [a for a in data if a["student_id"] == student_id]

    @staticmethod
    def get_by_date(date_str):
        data = load_data(AttendanceManager.FILE)
        return [a for a in data if a["date"] == date_str]

    @staticmethod
    def add(record):
        data = load_data(AttendanceManager.FILE)
        record["id"] = get_next_id(data)
        record["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.append(record)
        save_data(AttendanceManager.FILE, data)
        return record

    @staticmethod
    def delete(attendance_id):
        data = load_data(AttendanceManager.FILE)
        new_data = [a for a in data if a["id"] != attendance_id]
        if len(new_data) != len(data):
            save_data(AttendanceManager.FILE, new_data)
            return True
        return False
