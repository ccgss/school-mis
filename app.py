from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, g
from data_manager import (
    StudentManager, TeacherManager,
    CourseManager, GradeManager, AttendanceManager
)
from translations import t, get_lang, LANGUAGES

app = Flask(__name__)
app.secret_key = "school_mis_secret_key"


@app.context_processor
def inject_translation():
    return dict(t=t, current_lang=get_lang(), languages=LANGUAGES)


@app.route("/lang/<lang>")
def set_lang(lang):
    if lang in LANGUAGES:
        resp = make_response(redirect(request.referrer or url_for("dashboard")))
        resp.set_cookie("lang", lang, max_age=365 * 24 * 3600)
        return resp
    return redirect(url_for("dashboard"))


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
        "grade_record_count": len(grades),
        "attendance_record_count": len(attendance),
    }
    return render_template("dashboard.html", stats=stats)


# ===== Students =====

@app.route("/students")
def students():
    keyword = request.args.get("keyword", "")
    data = StudentManager.search(keyword) if keyword else StudentManager.get_all()
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
        flash(t("student_added"), "success")
        return redirect(url_for("students"))
    return render_template("student_form.html", student=None)


@app.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
def student_edit(student_id):
    student = StudentManager.get_by_id(student_id)
    if not student:
        flash(t("student_not_found"), "danger")
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
        flash(t("student_updated"), "success")
        return redirect(url_for("students"))
    return render_template("student_form.html", student=student)


@app.route("/students/delete/<int:student_id>")
def student_delete(student_id):
    StudentManager.delete(student_id)
    flash(t("student_deleted"), "success")
    return redirect(url_for("students"))


# ===== Teachers =====

@app.route("/teachers")
def teachers():
    keyword = request.args.get("keyword", "")
    data = TeacherManager.search(keyword) if keyword else TeacherManager.get_all()
    return render_template("teachers.html", teachers=data, keyword=keyword)


@app.route("/teachers/add", methods=["GET", "POST"])
def teacher_add():
    if request.method == "POST":
        td = {
            "teacher_id": request.form["teacher_id"],
            "name": request.form["name"],
            "gender": request.form["gender"],
            "subject": request.form["subject"],
            "phone": request.form.get("phone", ""),
            "email": request.form.get("email", ""),
        }
        TeacherManager.add(td)
        flash(t("teacher_added"), "success")
        return redirect(url_for("teachers"))
    return render_template("teacher_form.html", teacher=None)


@app.route("/teachers/edit/<int:teacher_id>", methods=["GET", "POST"])
def teacher_edit(teacher_id):
    teacher = TeacherManager.get_by_id(teacher_id)
    if not teacher:
        flash(t("teacher_not_found"), "danger")
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
        flash(t("teacher_updated"), "success")
        return redirect(url_for("teachers"))
    return render_template("teacher_form.html", teacher=teacher)


@app.route("/teachers/delete/<int:teacher_id>")
def teacher_delete(teacher_id):
    TeacherManager.delete(teacher_id)
    flash(t("teacher_deleted"), "success")
    return redirect(url_for("teachers"))


# ===== Courses =====

@app.route("/courses")
def courses():
    data = CourseManager.get_all()
    teachers_map = {tc["id"]: tc["name"] for tc in TeacherManager.get_all()}
    return render_template("courses.html", courses=data, teachers=teachers_map)


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
        flash(t("course_added"), "success")
        return redirect(url_for("courses"))
    teachers_list = TeacherManager.get_all()
    return render_template("course_form.html", course=None, teachers=teachers_list)


@app.route("/courses/edit/<int:course_id>", methods=["GET", "POST"])
def course_edit(course_id):
    course = CourseManager.get_by_id(course_id)
    if not course:
        flash(t("course_not_found"), "danger")
        return redirect(url_for("courses"))
    if request.method == "POST":
        updates = {
            "course_name": request.form["course_name"],
            "teacher_id": int(request.form["teacher_id"]),
            "schedule": request.form.get("schedule", ""),
            "classroom": request.form.get("classroom", ""),
        }
        CourseManager.update(course_id, updates)
        flash(t("course_updated"), "success")
        return redirect(url_for("courses"))
    teachers_list = TeacherManager.get_all()
    return render_template("course_form.html", course=course, teachers=teachers_list)


@app.route("/courses/delete/<int:course_id>")
def course_delete(course_id):
    CourseManager.delete(course_id)
    flash(t("course_deleted"), "success")
    return redirect(url_for("courses"))


# ===== Grades =====

@app.route("/grades")
def grades():
    data = GradeManager.get_all()
    students_map = {s["id"]: s["name"] for s in StudentManager.get_all()}
    courses_map = {c["id"]: c["course_name"] for c in CourseManager.get_all()}
    return render_template("grades.html", grades=data, students=students_map, courses=courses_map)


@app.route("/grades/add", methods=["GET", "POST"])
def grade_add():
    if request.method == "POST":
        gd = {
            "student_id": int(request.form["student_id"]),
            "course_id": int(request.form["course_id"]),
            "score": float(request.form["score"]),
            "exam_type": request.form.get("exam_type", ""),
            "semester": request.form.get("semester", ""),
        }
        GradeManager.add(gd)
        flash(t("grade_added"), "success")
        return redirect(url_for("grades"))
    students_list = StudentManager.get_all()
    courses_list = CourseManager.get_all()
    return render_template("grade_form.html", grade=None, students=students_list, courses=courses_list)


@app.route("/grades/delete/<int:grade_id>")
def grade_delete(grade_id):
    GradeManager.delete(grade_id)
    flash(t("grade_deleted"), "success")
    return redirect(url_for("grades"))


# ===== Attendance =====

@app.route("/attendance")
def attendance():
    data = AttendanceManager.get_all()
    students_map = {s["id"]: s["name"] for s in StudentManager.get_all()}
    courses_map = {c["id"]: c["course_name"] for c in CourseManager.get_all()}
    return render_template("attendance.html", records=data, students=students_map, courses=courses_map)


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
        flash(t("attendance_added"), "success")
        return redirect(url_for("attendance"))
    students_list = StudentManager.get_all()
    courses_list = CourseManager.get_all()
    today = date.today().isoformat()
    return render_template("attendance_form.html", record=None, students=students_list, courses=courses_list, today=today)


@app.route("/attendance/delete/<int:attendance_id>")
def attendance_delete(attendance_id):
    AttendanceManager.delete(attendance_id)
    flash(t("attendance_deleted"), "success")
    return redirect(url_for("attendance"))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
