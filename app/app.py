from flask import Flask
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
from views import *
from database import Database


if __name__ == '__main__':
    db = Database("127.0.0.1", 3306, "database", "database", "database")

    loginView = LoginView.as_view('login_view', database=db)
    app.add_url_rule('/login/', view_func=loginView, methods=['GET',])
    app.add_url_rule('/login/', view_func=loginView, methods=['POST',])

    registerView = RegisterView.as_view('register_view', database=db)
    app.add_url_rule('/register/', view_func=registerView, methods=['GET',])
    app.add_url_rule('/register/', view_func=registerView, methods=['POST',])
    
    app.run()
