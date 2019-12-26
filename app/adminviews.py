import flask
from flask import request, session, render_template, g
import models
from flask.views import MethodView
import logging
from datetime import datetime, timedelta


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

class Logout(MethodView):
    def get(self):
        if 'user_type' in session:
            session.pop('user_type', None)
            session.pop('first_name', None)
            session.pop('last_name', None)
            session.pop('userGId', None)
        return flask.redirect("/")

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
                return render_template(template,
                                       firstName=session['first_name'],
                                       lastName=session['last_name'])
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
        course = models.Course(name,description)
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
        group = models.Group(subjectId = subject, teacherId = teacher)
        try:
            self.db.insertGroup(group)
        except Exception as e:
            print(e)
            logging.exception("Connection to database failed")
            return flask.redirect("/")
        return flask.redirect("/admin/")

class AdminCreateLessonsView(UserView):
    def get(self, template="admin_create_lessons.html"):
        if self.permission == "admin":
            try:
                groups = self.db.getGroups(all=1)
                return render_template(template,groups = groups, firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
                return flask.redirect("/")
        return flask.redirect("/")

    def post(self, template="admin_lessons_created.html"):
        
        groupId = request.form.get("groupId", "")
        date = request.form.get("firstDay", "")
        quantity = request.form.get("quantity", "")
        classroom = request.form.get("classroom", "")
        timeValue = request.form.get("timeValue", "")
         
        format =  '%Y-%m-%d'
        for i in range(int(quantity)):
            datestr = datetime.strptime(date, format) + timedelta(days=7*i)
            lesson_date = str(datestr.year)+'-'+str(datestr.month)+'-'+str(datestr.day)
            lesson = models.Lesson(groupId = groupId, classroom = classroom, dateValue = lesson_date, timeValue = timeValue)
            try:
                self.db.insertLesson(lesson)
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
                return flask.redirect("/")
        return render_template(template, firstName=session['first_name'], lastName=session['last_name'])
        
        