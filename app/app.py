from flask import Flask
import os
from database import Database
from config import hostName, port, userName, password, database
from admin.app import admin_bp
from teacher.app import teacher_bp
from student.app import student_bp

if __name__ == '__main__':

    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)
    
    from views import *
    
    db = Database(hostName=hostName,
                 port=port,
                 userName=userName,
                 password=password,
                 database=database)

    indexView = IndexView.as_view('index_view')
    app.add_url_rule('/', view_func=indexView, methods=['GET',])

    loginView = LoginView.as_view('login_view', database=db)
    app.add_url_rule('/login/', view_func=loginView,methods=['GET',])
    app.add_url_rule('/login/', view_func=loginView, methods=['POST',])

    registerView = RegisterView.as_view('register_view', database=db)
    app.add_url_rule('/register/', view_func=registerView, methods=['GET',])
    app.add_url_rule('/register/', view_func=registerView, methods=['POST',])

    logoutView = Logout.as_view("logout_view")
    app.add_url_rule('/logout/', view_func=logoutView, methods=['GET',])
    
    app.run(debug=True)