
import flask
from flask import request, session, render_template, g
from models import User
from database import Database
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView

class IndexView(MethodView):
    def get(self):
        #session.pop('username', None)
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
            print(e) # use custom logger
            return render_template("fatalerror.html")

        if not user:
            return render_template("incorrectuser.html")
        
        if pbkdf2_sha256.verify(password, user.password):
            session['email'] = email
            session['username'] = user.firstName
            session['user_surname'] = user.lastName
            admin = self.db.get_admin_by_email(email)
            teacher = self.db.get_teacher_by_ident(user.userId)
            if admin:
                return flask.redirect("/admin/")
            elif teacher:
                return flask.redirect("/teacher/")
            else:
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

        try:
            if self.db.get_user_by_email(email):
                return render_template("incorrectemail.html")
        except Exception as e:
            print(e)
            return render_template("fatalerror.html") 

        us = User(firstName = firstName,
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
        if 'email' in session:
           return render_template("admin_view.html",firstName=session['username'], lastName=session['user_surname'])
        return flask.redirect("/")


class TeacherView(MethodView):
    def __init__(self, database):
        self.db = database

    def get(self):
        if 'email' in session:
            return render_template("teacher_view.html",firstName=session['username'], lastName=session['user_surname'])
        return flask.redirect("/")

class StudentView(MethodView):
    def __init__(self, database):
        self.db = database

    def get(self):
        if 'email' in session:
           return render_template("student_view.html",firstName=session['username'], lastName=session['user_surname'])
        return flask.redirect("/")

class Logout(MethodView):
    def get(self):
        if 'email' in session:
            session.pop('email', None)
            session.pop('username', None)
            session.pop('usersurname', None)
            return flask.redirect("/")
        return flask.redirect("/")



