import flask
from flask import request, session, render_template, g
from models import User, Course, Group
from database import Database
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView
import uuid

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
    
    def get(self):
        if self.permission == "admin": return flask.redirect("/admin/")
        if self.permission == "teacher": return flask.redirect("/teacher/")
        if self.permission == "student": return flask.redirect("/student/")
        return render_template('login.html')
    
    def post(self):
        email = request.form.get("email", "")
        password = request.form.get("pass", "")
        try:
            user = self.db.getUser(email)
        except Exception as e:
            print(e)
            return render_template("fatalerror.html")

        if not user:
            return render_template("incorrectuser.html")
        
        if pbkdf2_sha256.verify(password, user.password):
            session['user_type'] = user.user_type
            session['first_name'] = user.firstName
            session['last_name'] = user.lastName
            session['userGId'] = user.userGId
            if user.user_type == "admin": return flask.redirect("/admin/")
            if user.user_type == "teacher": return flask.redirect("/teacher/")
            return flask.redirect("/student/")
        return render_template("incorrectpass.html")

class RegisterView(IndexView):
    def __init__(self, database):
        super(RegisterView, self).__init__()
        self.db = database
    
    def get(self):
        if self.permission == "admin": return flask.redirect("/admin/")
        if self.permission == "teacher": return flask.redirect("/teacher/")
        if self.permission == "student": return flask.redirect("/student/")
        return render_template('register.html')
    
    def post(self):
        firstName = request.form.get("fname", "")
        lastName = request.form.get("lname", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        userGId = str(uuid.uuid1())

        try:
            if self.db.getUser(email):
                return render_template("incorrectemail.html")
        except Exception as e:
            print(e)
            return render_template("fatalerror.html") 

        user = User(userGId = userGId,
                 firstName = firstName,
                 lastName = lastName,
                 email = email,
                 password = pbkdf2_sha256.hash(password),
                 user_type = 'student',
                 active = True)
        try:        
            self.db.createUser(user)
        except Exception as e:
            print(e)
            return render_template("fatalerror.html") 
        return render_template('account_created.html')


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
    def get(self):
        if self.permission == "admin":
            return render_template("admin_view.html",firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")

class AdminUsersView(UserView):
    def user_error(self, template):
        try:
            teachers = self.db.getUsers(user_type="teacher")
            students = self.db.getUsers(user_type="student")
            return render_template(template,
                                    firstName=session['first_name'],
                                    lastName=session['last_name'],
                                    teachers=teachers,
                                    students=students,
                                    )
        except Exception as e:
            print(e)
            return render_template("fatal_error.html")
        
    def get(self):
        if self.permission == "admin":
            try:
                teachers = self.db.getUsers(user_type="teacher")
                students = self.db.getUsers(user_type="student")
                return render_template("users_management.html",
                                        firstName=session['first_name'],
                                        lastName=session['last_name'],
                                        teachers=teachers,
                                        students=students)
            except Exception as e:
                print(e)
        return flask.redirect("/")

    def post(self):
        user_email = request.form.get("user_email", "")
        option =  request.form.get("action", "")
        try:
            user = self.db.getUser(user_email)
        except Exception as e:
                print(e)
                return self.user_error("fatal_error.html")
        if option == "add_teacher":
            if user:
                if user.user_type == "student":
                    try:
                        user.user_type = "teacher"
                        self.db.updateUser(user, user_email)
                        return flask.redirect("/admin/users_management/")
                    except Exception as e:
                        print(e)
                        return self.user_error("fatal_error.html")    
                return self.user_error("already_added.html")
            return self.user_error("no_user.html")
        if option == "delete_teacher":
            if user:
                if user.active == 1:
                    try:
                        user.active = 0
                        self.db.updateUser(user, user_email)
                        return flask.redirect("/admin/users_management/")
                    except Exception as e:
                        print(e)
                        return self.user_error("fatal_error.html")
                return self.user_error("already_deleted.html")   
            return self.user_error("no_user.html")
        if option == "delete_student":
                if user:
                    if user.active == 1:
                        try:
                            user.active = 0
                            self.db.updateUser(user, user_email)
                            return flask.redirect("/admin/users_management/")
                        except Exception as e:
                            print(e)
                            return self.user_error("fatal_error.html")
                        return self.user_error("already_deleted.html")
                return self.user_error("no_user.html")
            
        if option == "reboot_student":
            if user:
                if user.active == 0:
                    try:
                        user.active = 1
                        self.db.updateUser(user, user_email)
                        return flask.redirect("/admin/users_management/")
                    except Exception as e:
                        print(e)
                        return self.user_error("fatal_error.html")
                return self.user_error("already_added.html")
            return self.user_error("no_user.html")

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
            self.db.createCourse(course)
        except Exception as e:
            print(e)
            return flask.redirect("/")
        return flask.redirect("/admin/")

class AdminCoursesView(UserView):
    def get(self):
        if self.permission == "admin":
            courses = self.db.getCourses()
            return render_template("list_courses.html",courses=courses, firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")

class AdminCreateGroupView(UserView):
    def get(self):
        if self.permission == "admin":
            teachers = self.db.getUsers("teacher")
            courses = self.db.getCourses()
            return render_template("creategroup.html",teachers=teachers, courses=courses, firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")

    def post(self):
        subject = request.form.get("subject", "")
        teacher = request.form.get("teacher", "")
        group = Group(subjectId = subject, teacherId = teacher)
        try:
            self.db.createGroup(group)
        except Exception as e:
            print(e)
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
            courses = self.db.getCourses()
            return render_template("student_courses.html",courses=courses, firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")

class StudentGroupsView(UserView):
    def get(self, subjectId):
        if self.permission == "student":
            groups = self.db.getGroups(subjectId)
            for group in groups:
                teacher = self.db.getUser(userGId=group.teacherId)
                group.teacherId = teacher.firstName + ' ' + teacher.lastName
            return render_template("student_groups.html", groups = groups,firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")

class StudentLessonsView(UserView):
    def get(self, groupId):
        if self.permission == "student":
            lessons = self.db.getLessons(groupId)
            return render_template("student_lessons.html", lessons = lessons,firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")
    

class Logout(MethodView):
    def get(self):
        if 'user_type' in session:
            session.pop('user_type', None)
            session.pop('first_name', None)
            session.pop('last_name', None)
            session.pop('userGId', None)
            return flask.redirect("/")
        return flask.redirect("/")



