from app import app
import flask
from flask import request
from models import User, Database
from passlib.hash import pbkdf2_sha256

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return "<h1>Jestes zalogowany</h1>"
    else:
        return """<h1>Hello world</h1>
                <h3> You are on index site </h3>
                <p> Welcome to Akademia Programowania </p>
                <button><a href='login'>Zaloguj</a></button>
                <button><a href='register'>Zarejestruj się</a></button>"""
   
@app.route("/register", methods=["GET", "POST"])
def register():
        return """ <form action='/registered' method="POST"> 
                First name: <input type='text' name='fname' required><br>
                Last name: <input type='text' name='lname' required><br>
                Email: <input type='email' name='email' required><br>
                Password: <input type='password' name='password' required><br>
                <label><input type="checkbox" required> Akceptuje regulamin</label>
                <input type='submit' value='Submit'>
                </form> """

@app.route("/login")
def login():
    return """ <form action='/logged' method="POST"> 
                Login: <input type='text' name='email' required><br>
                Hasło: <input type='password' name='pass' required><br>
                <input type='submit' value='Zaloguj'>
                </form> """

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
        password = pbkdf2_sha256.hash(request.form["password"])
        u = User()
        u.first_name = name
        u.last_name = surname
        u.email = email
        u.password = password
        Database.add_user(Database, u)
        return "Utworzyłeś konto <button><a href='login'>Zaloguj się</a></button> "
    else:
        return flask.redirect('/')
