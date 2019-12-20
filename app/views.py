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


class Logout(MethodView):
    def get(self):
        if 'user_type' in session:
            session.pop('user_type', None)
            session.pop('first_name', None)
            session.pop('last_name', None)
            session.pop('userGId', None)
        return flask.redirect("/")



