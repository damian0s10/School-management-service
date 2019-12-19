import flask
from flask import request, session, render_template, g
from models import *
from database import Database
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView
import uuid
import logging


class IndexView(MethodView):
    def __init__(self):
        self.permission = None
        self.authorization()
    
    def authorization(self):
        if 'user_type' in session:
            if session['user_type'] == "admin": self.permission = "admin"
            elif session['user_type'] == "teacher": self.permission = "teacher"
            elif session['user_type'] == "student": self.permission = "student"
            else: self.permission = None
        else: self.permission = None

    def get(self):
        if self.permission == "admin": return render_template("admin_view.html",firstName=session['first_name'], lastName=session['last_name'])
        if self.permission == "teacher": return render_template("teacher_view.html",firstName=session['first_name'], lastName=session['last_name'])
        if self.permission == "student": return render_template("student_view.html",firstName=session['first_name'], lastName=session['last_name'])
        return render_template('index.html')
        

class LoginView(IndexView):
    def __init__(self, database):
        super(LoginView, self).__init__()
        self.db = database
    
    def get(self, template='login.html'):
        if self.permission == "admin": return flask.redirect("/admin/")
        if self.permission == "teacher": return flask.redirect("/teacher/")
        if self.permission == "student": return flask.redirect("/student/")
        return render_template(template)
    
    def post(self):
        email = request.form.get("email", "")
        password = request.form.get("pass", "")
        try:
            user = self.db.getUser(email)
        except Exception as e:
            print(e)
            logging.exception("Connection to database failed")
            return self.get(template="fatalerror.html")

        if not user:
            return self.get(template="incorrectuser.html")
        
        if pbkdf2_sha256.verify(password, user.password):
            session['user_type'] = user.user_type
            session['first_name'] = user.firstName
            session['last_name'] = user.lastName
            session['userGId'] = user.userGId
            if user.user_type == "admin": return flask.redirect("/admin/")
            if user.user_type == "teacher": return flask.redirect("/teacher/")
            return flask.redirect("/student/")
        return self.get(template="incorrectpass.html")

class RegisterView(IndexView):
    def __init__(self, database):
        super(RegisterView, self).__init__()
        self.db = database
    
    def get(self, template='register.html'):
        if self.permission == "admin": return flask.redirect("/admin/")
        if self.permission == "teacher": return flask.redirect("/teacher/")
        if self.permission == "student": return flask.redirect("/student/")
        return render_template(template)
    
    def post(self):
        firstName = request.form.get("fname", "")
        lastName = request.form.get("lname", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        userGId = str(uuid.uuid1())

        try:
            if self.db.getUser(email):
                return self.get(template="incorrectemail.html")
        except Exception as e:
            print(e)
            logging.exception("Connection to database failed")
            return self.get(template="fatalerror.html") 

        user = User(
                 userGId = userGId,
                 firstName = firstName,
                 lastName = lastName,
                 email = email,
                 password = pbkdf2_sha256.hash(password),
                 user_type = 'student',
                 active = True)
        try:        
            self.db.insertUser(user)
        except Exception as e:
            print(e)
            logging.exception("Connection to database failed")
            return self.get(template="fatalerror.html") 
        return self.get(template='account_created.html')


class UserView(MethodView):
    def __init__(self, database):
        self.db = database
        self.permission = None
        self.authorization()

    def authorization(self):
        if 'user_type' in session:
            if session['user_type'] == "admin": self.permission = "admin"
            elif session['user_type'] == "teacher": self.permission = "teacher"
            elif session['user_type'] == "student": self.permission = "student"
            else: self.permission = None
        else: self.permission = None

class AdminView(UserView):
    def get(self, template="admin_view.html"):
        if self.permission == "admin":
            return render_template(
                template,
                firstName=session['first_name'], 
                lastName=session['last_name'])
        return flask.redirect("/")

class AdminUsersView(UserView):
    def get(self, template="users_management.html"):
        if self.permission == "admin":
            try:
                teachers = self.db.getUsers(user_type="teacher")
                students = self.db.getUsers(user_type="student")
                return render_template(template,
                                       firstName=session['first_name'],
                                       lastName=session['last_name'],
                                       teachers=teachers,
                                       students=students)
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

    def post(self):
        user_email = request.form.get("user_email", "")
        option =  request.form.get("action", "")
        try:
            user = self.db.getUser(user_email)
        except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
                return self.get(template="fatal_error.html")
        if option == "add_teacher":
            if user:
                if user.user_type == "student":
                    try:
                        user.user_type = "teacher"
                        self.db.updateUser(user, user_email)
                        return flask.redirect("/admin/users_management/")
                    except Exception as e:
                        print(e)
                        logging.exception("Connection to database failed")
                        return self.get(template="fatal_error.html")    
                return self.get(template="already_added.html")
            return self.get(template="no_user.html")
        if option == "delete_teacher":
            if user:
                if user.active == 1:
                    try:
                        user.active = 0
                        self.db.updateUser(user, user_email)
                        return flask.redirect("/admin/users_management/")
                    except Exception as e:
                        print(e)
                        logging.exception("Connection to database failed")
                        return self.get(template="fatal_error.html")
                return self.get(template="already_deleted.html")   
            return self.get(template="no_user.html")
        if option == "delete_student":
                if user:
                    if user.active == 1:
                        try:
                            user.active = 0
                            self.db.updateUser(user, user_email)
                            return flask.redirect("/admin/users_management/")
                        except Exception as e:
                            print(e)
                            logging.exception("Connection to database failed")
                            return self.get(template="fatal_error.html")
                        return self.get(template="already_deleted.html")
                return self.get(template="no_user.html")
            
        if option == "reboot_student":
            if user:
                if user.active == 0:
                    try:
                        user.active = 1
                        self.db.updateUser(user, user_email)
                        return flask.redirect("/admin/users_management/")
                    except Exception as e:
                        print(e)
                        logging.exception("Connection to database failed")
                        return self.get(template="fatal_error.html")
                return self.get(template="already_added.html")
            return self.get(template="no_user.html")

        return flask.redirect("/admin/users_management/")
        
    
class AdminAddCourseView(UserView):
    def get(self):
        if self.permission == "admin":
            return render_template("createcourse.html",firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")

    def post(self):
        name = request.form.get("name", "")
        description = request.form.get("description", "")
        course = Course(name,description)
        try:
            self.db.insertCourse(course)
        except Exception as e:
            print(e)
            logging.exception("Connection to database failed")
            return flask.redirect("/")
        return flask.redirect("/admin/")

class AdminCoursesView(UserView):
    def get(self):
        if self.permission == "admin":
            try:
                courses = self.db.getCourses()
                return render_template("list_courses.html",courses=courses, firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

class AdminCreateGroupView(UserView):
    def get(self):
        if self.permission == "admin":
            try:
                teachers = self.db.getUsers("teacher")
                courses = self.db.getCourses()
                return render_template("creategroup.html",teachers=teachers, courses=courses, firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

    def post(self):
        subject = request.form.get("subject", "")
        teacher = request.form.get("teacher", "")
        group = Group(subjectId = subject, teacherId = teacher)
        try:
            self.db.insertGroup(group)
        except Exception as e:
            print(e)
            logging.exception("Connection to database failed")
            return flask.redirect("/")
        return flask.redirect("/admin/")

class TeacherView(UserView):
    def get(self):
        if self.permission == "teacher":
            return render_template("teacher_view.html",firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")

class StudentView(UserView):
    def get(self):
        if self.permission == "student":
            return render_template("student_view.html",firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")

class StudentCoursesView(UserView):
    def get(self):
        if self.permission == "student":
            try:
                courses = self.db.getCourses()
                return render_template("student_courses.html",courses=courses, firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

class StudentGroupsView(UserView):
    def get(self, subjectId):
        if self.permission == "student":
            try:
                groups = self.db.getGroups(subjectId)
                for group in groups:
                    teacher = self.db.getUser(userGId=group.teacherId)
                    group.teacherId = teacher.firstName + ' ' + teacher.lastName
                return render_template("student_groups.html", groups = groups,firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

class StudentLessonsView(UserView):
    def get(self, groupId, template="student_lessons.html"):
        if self.permission == "student":
            try:
                lessons = self.db.getLessons(groupId)
                return render_template(template, lessons = lessons,firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

    def post(self, groupId, template="student_added_to_group.html"):
        if self.permission == "student":
            userGId = session["userGId"]
            groupId = request.form.get("groupId", "")
            match = Match(groupId = groupId, studentId = userGId, active = 1)
            try:
                self.db.insertMatch(match)
                return render_template(template,firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")    
        return flask.redirect("/")

class TeacherCreateMessageView(UserView):
    def get(self,template="teacher_create_message.html"):
        if self.permission == "teacher":
            try:
                groups = self.db.getGroups(teacherId = session['userGId'])
                return render_template(template,groups = groups,firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

    def post(self):
        if self.permission == "teacher":
            groupId = request.form.get("groupId", "")
            message = request.form.get("message", "")
            m = Message(userGId = session["userGId"], groupId = groupId, message = message)
            try:
                self.db.insertMessage(m)
                return flask.redirect("/news")
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")


class Logout(MethodView):
    def get(self):
        if 'user_type' in session:
            session.pop('user_type', None)
            session.pop('first_name', None)
            session.pop('last_name', None)
            session.pop('userGId', None)
        return flask.redirect("/")



