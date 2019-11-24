from app import app
import flask
from flask import request, session, render_template, g
from models import User
from database import Database
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView


@app.route("/")
def index():
    return render_template('index.html')

class LoginView(MethodView):
    def __init__(self, database):
        self.db = database
    
    def get(self):
        return render_template('login.html')
    
    def post(self):
        session.pop('user', None)
        email = request.form.get("email", "")
        password = request.form.get("pass", "")
        try:
            user = self.db.get_user_by_email(email)
        except Exception as e:
            print(e) # use custom logger
            return render_template("incorrectuser.html") # TODO: change to other html
 
        if not user:
            return render_template("incorrectuser.html")
        
        if pbkdf2_sha256.verify(password, user.password):
            session['user'] = email
            return render_template("slogged.html", firstName = user.firstName, lastName = user.lastName)
        
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
            # TODO: add handling of catch
            print(e)
            return render_template("incorrectemail.html") 

        u = User(firstName = firstName,
                 lastName = lastName,
                 email = email,
                 password = pbkdf2_sha256.hash(password),
                 active = True)
        try:        
            self.db.add_user(u)
        except Exception as e:
            # TODO: add handling of catch
            return 

        return "Utworzyłeś konto <button><a href='/login'>Zaloguj się</a></button> "


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']   

@app.route("/logout")
def logout():
    session.pop('user', None)
    return flask.redirect('/')


@app.route("/news")
def news():
    return render_template('news.html')

@app.route("/courses")
def courses():
    return render_template('courses.html')

@app.route("/groups")
def ngroups():
    return render_template('groups.html')
@app.route("/grades")
def grades():
    return render_template('grades.html')
