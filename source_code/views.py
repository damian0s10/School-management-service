from app import app
import flask
from flask import request
@app.route("/")
def index():
    return "<h1>Hello world</h1>"+"<h3> You are on index site </h3>"+"<p> Welcome to Akademia Programowania </p>"
   
@app.route("/register", methods=["GET", "POST"])
def register():
        return """ <form action='/registered' method="POST"> 
                First name: <input type='text' name='fname'><br>
                Last name: <input type='text' name='lname'><br>
                Email: <input type='email' name='email'><br>
                Password: <input type='password' name='password'><br>
                <input type='submit' value='Submit'>
                </form> """

@app.route("/login")
def login():
    return "<h3> This is the login site </h3>"

@app.route("/logout")
def logout():
    return flask.redirect('/')

@app.route("/registered", methods=["GET", "POST"])
def registered():
    if request.method == "POST":
        name = request.form["fname"]
        surname = request.form["lname"]
        email = request.form["email"]
        password = request.form["password"]
        return "Witaj" + name + " " + surname + " " + email + " " + password
    else:
        return flask.redirect('/')