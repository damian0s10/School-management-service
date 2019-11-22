from app import app
import flask
from flask import request, session, render_template, g
from models import User, Database
from passlib.hash import pbkdf2_sha256


@app.route("/")
def index():
    return render_template('index.html')
   
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template('register.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']   

@app.route("/logged", methods=["GET", "POST"])
def logged():
    if request.method == "POST":
        session.pop('user', None)
        email = request.form["email"]
        password = request.form["pass"]
        user = Database.get_user_by_email(Database,email)
        if(user):
            if(pbkdf2_sha256.verify(password, user.password)):
                session['user'] = email
                return render_template("slogged.html", firstName = user.firstName, lastName = user.lastName)
            else:
                return render_template("incorrectpass.html")
        else:
            return render_template("incorrectuser.html")
    else:
        return flask.redirect('/')


@app.route("/logout")
def logout():
    session.pop('user', None)
    return flask.redirect('/')

@app.route("/registered", methods=["GET", "POST"])
def registered():
    if request.method == "POST":
        firstName = request.form["fname"]
        lastName = request.form["lname"]
        email = request.form["email"]
        isAvailable = Database.get_user_by_email(Database, email)
        if(isAvailable):
            return render_template("incorrectemail.html")
        else: 
            password = pbkdf2_sha256.hash(request.form["password"])
            u = User(firstName = firstName,
                     lastName = lastName,
                     email = email,
                     password = password,
                     active = True)
            Database.add_user(Database, u)
            return "Utworzyłeś konto <button><a href='/login'>Zaloguj się</a></button> "
            
    else:
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
