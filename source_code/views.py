from app import app
import flask
from flask import request, session, render_template
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
    

@app.route("/logged", methods=["GET", "POST"])
def logged():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]
        user = Database.get_user_by_email(Database,email)
        if(user):
            if(pbkdf2_sha256.verify(password, user.password)):
                return "Jesteś zalogowany jako " + user.first_name + \
                "<a href='/logout'>Wyloguj</a>"
            else:
                return """Podałeś nieprawidłowe hasło
                        <a href='/login'>Powrót</a>"""
        else:
            return """Nie ma takiego użytkownika
                        <a href='/login'>Powrót</a>"""
    else:
        return flask.redirect('/')


@app.route("/logout")
def logout():
    return flask.redirect('/')

@app.route("/registered", methods=["GET", "POST"])
def registered():
    if request.method == "POST":
        name = request.form["fname"]
        surname = request.form["lname"]
        email = request.form["email"]
        isAvailable = Database.get_user_by_email(Database, email)
        if(isAvailable):
            return "Konto o tym adresie email juz istnieje <button><a href='/register'>Spróbuj ponownie</a></button> "
        else: 
            password = pbkdf2_sha256.hash(request.form["password"])
            u = User()
            u.first_name = name
            u.last_name = surname
            u.email = email
            u.password = password
            Database.add_user(Database, u)
            return "Utworzyłeś konto <button><a href='/login'>Zaloguj się</a></button> "
            
    else:
        return flask.redirect('/')
