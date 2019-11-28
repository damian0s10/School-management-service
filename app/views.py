import flask
from flask import request, session, render_template, g
from models import User
from database import Database
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView
import uuid

class IndexView(MethodView):
    def get(self):
        return render_template('index.html')
        

class LoginView(MethodView):
    def __init__(self, database):
        self.db = database
    
    def get(self):
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
            session['userGId'] = user.userGId
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
    def get(self):
        if 'userGId' in session:
            try:
                if self.db.get_user_by_id(session['userGId']).user_type == "admin":
                    return render_template("admin_view.html",firstName=session['first_name'], lastName=session['last_name'])
                return flask.redirect("/")
            except Exception as e:
                print(e)
                return render_template("fatalerror.html")
        return flask.redirect("/")


class TeacherView(MethodView):
    def __init__(self, database):
        self.db = database
    def get(self):
        if 'userGId' in session:
            try:
                if self.db.get_user_by_id(session['userGId']).user_type == "teacher":
                    return render_template("teacher_view.html",firstName=session['first_name'], lastName=session['last_name'])
                return flask.redirect("/")
            except Exception as e:
                print(e)
                return render_template("fatalerror.html")
        return flask.redirect("/")

class StudentView(MethodView):
    def __init__(self, database):
        self.db = database
    def get(self):
        if 'userGId' in session:
            try:
                if self.db.get_user_by_id(session['userGId']).user_type == "teacher":
                    if session['userGId'] == self.db.get_user_by_id(session['userGId']):
                        return render_template("student_view.html",firstName=session['first_name'], lastName=session['last_name'])
                    return flask.redirect("/")
            except Exception as e:
                print(e)
                return render_template("fatalerror.html")
        return flask.redirect("/")

class Logout(MethodView):
    def get(self):
        if 'userGId' in session:
            session.pop('userGId', None)
            session.pop('first_name', None)
            session.pop('last_name', None)
            return flask.redirect("/")
        return flask.redirect("/")



