import flask
from flask import request, session, render_template, g
from models import User, Course, Group
from database import Database
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView
import uuid

class IndexView(MethodView):
    def get(self):
        if 'user_type' in session:
            if session['user_type'] == "admin": return flask.redirect("/admin/")
            if session['user_type'] == "teacher": return flask.redirect("/teacher/")
            if session['user_type'] == "student": return flask.redirect("/student/")
        return render_template('index.html')
        

class LoginView(MethodView):
    def __init__(self, database):
        self.db = database
    
    def get(self):
        if 'user_type' in session:
            if session['user_type'] == "admin": return flask.redirect("/admin/")
            if session['user_type'] == "teacher": return flask.redirect("/teacher/")
            if session['user_type'] == "student": return flask.redirect("/student/")
        return render_template('login.html')
    
    def post(self):
        email = request.form.get("email", "")
        password = request.form.get("pass", "")
        try:
            user = self.db.get_user_by_email(email)
        except Exception as e:
            print(e)
            return render_template("fatalerror.html")

        if not user:
            return render_template("incorrectuser.html")
        
        if pbkdf2_sha256.verify(password, user.password):
            session['user_type'] = user.user_type
            session['first_name'] = user.firstName
            session['last_name'] = user.lastName
            if user.user_type == "admin": return flask.redirect("/admin/")
            if user.user_type == "teacher": return flask.redirect("/teacher/")
            return flask.redirect("/student/")
        return render_template("incorrectpass.html")

class RegisterView(MethodView):
    def __init__(self, database):
        self.db = database
    
    def get(self):
        if 'user_type' in session:
            if session['user_type'] == "admin": return flask.redirect("/admin/")
            if session['user_type'] == "teacher": return flask.redirect("/teacher/")
            if session['user_type'] == "student": return flask.redirect("/student/")
        return render_template('register.html')
    
    def post(self):
        firstName = request.form.get("fname", "")
        lastName = request.form.get("lname", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        userGId = str(uuid.uuid1())

        try:
            if self.db.get_user_by_email(email):
                return render_template("incorrectemail.html")
        except Exception as e:
            print(e)
            return render_template("fatalerror.html") 

        us = User(userGId = userGId,
                 firstName = firstName,
                 lastName = lastName,
                 email = email,
                 password = pbkdf2_sha256.hash(password),
                 user_type = 'student',
                 active = True)
        try:        
            self.db.add_user(us)
        except Exception as e:
            print(e)
            return render_template("fatalerror.html") 
        return render_template('account_created.html')


class AdminView(MethodView):
    def __init__(self, database):
        self.db = database
        self.permission = None
        self.authorization()

    def authorization(self):
        if 'user_type' in session:
            if session['user_type'] == "admin": self.permission = "admin"
            if session['user_type'] == "teacher": self.permission = "teacher"
            if session['user_type'] == "student": self.permission = "student"
            else: pass
        return flask.redirect("/")
    def get(self):
        if 'user_type' in session:
            if self.permission == "admin":
                return render_template("admin_view.html",firstName=session['first_name'], lastName=session['last_name'])
            return flask.redirect("/")
        return flask.redirect("/")

class adminAddCourseView(AdminView):
    def get(self):
        if 'user_type' in session:
            if self.permission == "admin":
                return render_template("createcourse.html",firstName=session['first_name'], lastName=session['last_name'])
            return flask.redirect("/")
        return flask.redirect("/")
    def post(self):
        name = request.form.get("name", "")
        description = request.form.get("description", "")
        course = Course(name,description)
        try:
            self.db.add_course(course)
        except Exception as e:
            print(e)
            return flask.redirect("/")
        return flask.redirect("/admin/")

class adminCoursesView(AdminView):
    def get(self):
        if 'user_type' in session:
            if self.permission == "admin":
                courses = self.db.get_all_courses()
                return render_template("listcourses.html",courses=courses, firstName=session['first_name'], lastName=session['last_name'])
            return flask.redirect("/")
        return flask.redirect("/")

class adminCreateGroupView(AdminView):
    def get(self):
        if 'user_type' in session:
            if self.permission == "admin":
                teachers = self.db.get_all_teachers()
                courses = self.db.get_all_courses()
                return render_template("creategroup.html",teachers=teachers, courses=courses, firstName=session['first_name'], lastName=session['last_name'])
            return flask.redirect("/")
        return flask.redirect("/")
    def post(self):
        subject = request.form.get("subject", "")
        teacher = request.form.get("teacher", "")
        group = Group(subjectId = subject, teacherId = teacher)
        try:
            self.db.add_group(group)
        except Exception as e:
            print(e)
            return flask.redirect("/")
        return flask.redirect("/admin/")

class TeacherView(AdminView):
    def get(self):
        if 'user_type' in session:
            if self.permission == "teacher":
                    return render_template("teacher_view.html",firstName=session['first_name'], lastName=session['last_name'])
            return flask.redirect("/")
        return flask.redirect("/")

class StudentView(AdminView):
    def get(self):
        if 'user_type' in session:
            if self.permission == "student":
                return render_template("student_view.html",firstName=session['first_name'], lastName=session['last_name'])
            return flask.redirect("/")
        return flask.redirect("/")

class Logout(MethodView):
    def get(self):
        if 'user_type' in session:
            session.pop('user_type', None)
            session.pop('first_name', None)
            session.pop('last_name', None)
            return flask.redirect("/")
        return flask.redirect("/")



