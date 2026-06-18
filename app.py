from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from data_manager import (
    ensure_data_file, StudentManager, TeacherManager,
    CourseManager, GradeManager, AttendanceManager
)

app = Flask(__name__)
app.secret_key = "school_mis_secret_key"

for fname, default in [
    ("students.json", []),
    ("teachers.json", []),
    ("courses.json", []),
    ("grades.json", []),
    ("attendance.json", []),
]:
    ensure_data_file(fname, default)

@app.route("/")
def dashboard():
    students = StudentManager.get_all()
    teachers = TeacherManager.get_all()
    courses = CourseManager.get_all()
    grades = GradeManager.get_all()
    attendance = AttendanceManager.get_all()

    stats = {
        "student_count": len(students),
        "teacher_count": len(teachers),
        "course_count": len(courses),
        "grade_count": len(grades),
        "attendance_count": len(attendance),
    }
    return render_template("dashboard.html", stats=stats)

@app.route("/students")
def students():
    keyword = request.args.get("keyword", "")
    if keyword:
        data = StudentManager.search(keyword)
    else:
        data = StudentManager.get_all()
    return render_template("students.html", students=data, keyword=keyword)

@app.route("/students/add", methods=["GET", "POST"])
def student_add():
    if request.method == "POST":
        s = {
            "student_id": request.form["student_id"],
            "name": request.form["name"],
            "gender": request.form["gender"],
            "class_name": request.form["class_name"],
            "phone": request.form.get("phone", ""),
            "email": request.form.get("email", ""),
            "address": request.form.get("address", ""),
        }
        StudentManager.add(s)
        flash("学生添加成功！", "success")
        return redirect(url_for("students"))
    return render_template("student_form.html", student=None)

@app.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
def student_edit(student_id):
    student = StudentManager.get_by_id(student_id)
    if not student:
        flash("学生不存在！", "danger")
        return redirect(url_for("students"))
    if request.method == "POST":
        updates = {
            "student_id": request.form["student_id"],
            "name": request.form["name"],
            "gender": request.form["gender"],
            "class_name": request.form["class_name"],
            "phone": request.form.get("phone", ""),
            "email": request.form.get("email", ""),
            "address": request.form.get("address", ""),
        }
        StudentManager.update(student_id, updates)
        flash("学生信息更新成功！", "success")
        return redirect(url_for("students"))
    return render_template("student_form.html", student=student)

@app.route("/students/delete/<int:student_id>")
def student_delete(student_id):
    StudentManager.delete(student_id)
    flash("学生已删除！", "success")
    return redirect(url_for("students"))

@app.route("/teachers")
def teachers():
    keyword = request.args.get("keyword", "")
    if keyword:
        data = TeacherManager.search(keyword)
    else:
        data = TeacherManager.get_all()
    return render_template("teachers.html", teachers=data, keyword=keyword)

@app.route("/teachers/add", methods=["GET", "POST"])
def teacher_add():
    if request.method == "POST":
        t = {
            "teacher_id": request.form["teacher_id"],
            "name": request.form["name"],
            "gender": request.form["gender"],
            "subject": request.form["subject"],
            "phone": request.form.get("phone", ""),
            "email": request.form.get("email", ""),
        }
        TeacherManager.add(t)
        flash("教师添加成功！", "success")
        return redirect(url_for("teachers"))
    return render_template("teacher_form.html", teacher=None)

@app.route("/teachers/edit/<int:teacher_id>", methods=["GET", "POST"])
def teacher_edit(teacher_id):
    teacher = TeacherManager.get_by_id(teacher_id)
    if not teacher:
        flash("教师不存在！", "danger")
        return redirect(url_for("teachers"))
    if request.method == "POST":
        updates = {
            "teacher_id": request.form["teacher_id"],
            "name": request.form["name"],
            "gender": request.form["gender"],
            "subject": request.form["subject"],
            "phone": request.form.get("phone", ""),
            "email": request.form.get("email", ""),
        }
        TeacherManager.update(teacher_id, updates)
        flash("教师信息更新成功！", "success")
        return redirect(url_for("teachers"))
    return render_template("teacher_form.html", teacher=teacher)

@app.route("/teachers/delete/<int:teacher_id>")
def teacher_delete(teacher_id):
    TeacherManager.delete(teacher_id)
    flash("教师已删除！", "success")
    return redirect(url_for("teachers"))

@app.route("/courses")
def courses():
    data = CourseManager.get_all()
    teachers = {t["id"]: t["name"] for t in TeacherManager.get_all()}
    return render_template("courses.html", courses=data, teachers=teachers)

@app.route("/courses/add", methods=["GET", "POST"])
def course_add():
    if request.method == "POST":
        c = {
            "course_name": request.form["course_name"],
            "teacher_id": int(request.form["teacher_id"]),
            "schedule": request.form.get("schedule", ""),
            "classroom": request.form.get("classroom", ""),
        }
        CourseManager.add(c)
        flash("课程添加成功！", "success")
        return redirect(url_for("courses"))
    teachers = TeacherManager.get_all()
    return render_template("course_form.html", course=None, teachers=teachers)

@app.route("/courses/edit/<int:course_id>", methods=["GET", "POST"])
def course_edit(course_id):
    course = CourseManager.get_by_id(course_id)
    if not course:
        flash("课程不存在！", "danger")
        return redirect(url_for("courses"))
    if request.method == "POST":
        updates = {
            "course_name": request.form["course_name"],
            "teacher_id": int(request.form["teacher_id"]),
            "schedule": request.form.get("schedule", ""),
            "classroom": request.form.get("classroom", ""),
        }
        CourseManager.update(course_id, updates)
        flash("课程信息更新成功！", "success")
        return redirect(url_for("courses"))
    teachers = TeacherManager.get_all()
    return render_template("course_form.html", course=course, teachers=teachers)

@app.route("/courses/delete/<int:course_id>")
def course_delete(course_id):
    CourseManager.delete(course_id)
    flash("课程已删除！", "success")
    return redirect(url_for("courses"))

@app.route("/grades")
def grades():
    data = GradeManager.get_all()
    students = {s["id"]: s["name"] for s in StudentManager.get_all()}
    courses = {c["id"]: c["course_name"] for c in CourseManager.get_all()}
    return render_template("grades.html", grades=data, students=students, courses=courses)

@app.route("/grades/add", methods=["GET", "POST"])
def grade_add():
    if request.method == "POST":
        g = {
            "student_id": int(request.form["student_id"]),
            "course_id": int(request.form["course_id"]),
            "score": float(request.form["score"]),
            "exam_type": request.form.get("exam_type", "期中"),
            "semester": request.form.get("semester", ""),
        }
        GradeManager.add(g)
        flash("成绩录入成功！", "success")
        return redirect(url_for("grades"))
    students = StudentManager.get_all()
    courses = CourseManager.get_all()
    return render_template("grade_form.html", grade=None, students=students, courses=courses)

@app.route("/grades/delete/<int:grade_id>")
def grade_delete(grade_id):
    GradeManager.delete(grade_id)
    flash("成绩已删除！", "success")
    return redirect(url_for("grades"))

@app.route("/attendance")
def attendance():
    data = AttendanceManager.get_all()
    students = {s["id"]: s["name"] for s in StudentManager.get_all()}
    courses = {c["id"]: c["course_name"] for c in CourseManager.get_all()}
    return render_template("attendance.html", records=data, students=students, courses=courses)

@app.route("/attendance/add", methods=["GET", "POST"])
def attendance_add():
    if request.method == "POST":
        a = {
            "student_id": int(request.form["student_id"]),
            "course_id": int(request.form["course_id"]),
            "date": request.form["date"],
            "status": request.form["status"],
            "remark": request.form.get("remark", ""),
        }
        AttendanceManager.add(a)
        flash("考勤记录添加成功！", "success")
        return redirect(url_for("attendance"))
    students = StudentManager.get_all()
    courses = CourseManager.get_all()
    return render_template("attendance_form.html", record=None, students=students, courses=courses, today=date.today().isoformat())

@app.route("/attendance/delete/<int:attendance_id>")
def attendance_delete(attendance_id):
    AttendanceManager.delete(attendance_id)
    flash("考勤记录已删除！", "success")
    return redirect(url_for("attendance"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
