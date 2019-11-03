from app import app
import flask

@app.route("/")
def index():
    return "<h1>Hello world</h1>"+"<h3> You are on index site </h3>"+"<p> Welcome to Akademia Programowania </p>"
   
@app.route("/register")
def register():
    return "<h3> This is the register site</h3>"

@app.route("/login")
def login():
    return "<h3> This is the login site </h3>"

@app.route("/logout")
def logout():
    return flask.redirect('/')


