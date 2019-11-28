from flask import Flask
import os
from database import Database
from views import *

if __name__ == '__main__':
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    db = Database("localhost", 3306, "database", "database", "database")

    indexView = IndexView.as_view('index_view')
    app.add_url_rule('/', view_func=indexView, methods=['GET',])

    loginView = LoginView.as_view('login_view', database=db)
    app.add_url_rule('/login/', view_func=loginView,methods=['GET',])
    app.add_url_rule('/login/', view_func=loginView, methods=['POST',])

    registerView = RegisterView.as_view('register_view', database=db)
    app.add_url_rule('/register/', view_func=registerView, methods=['GET',])
    app.add_url_rule('/register/', view_func=registerView, methods=['POST',])
    
    studentView = StudentView.as_view('student_view', database = db)
    app.add_url_rule('/student/', view_func=studentView, methods=['GET',])

    adminView = AdminView.as_view('admin_view', database = db)
    app.add_url_rule('/admin/', view_func=adminView, methods=['GET',])

    adminAddCourseView = adminAddCourseView.as_view('adminAddCourseView', database = db)
    app.add_url_rule('/admin/createcourse/', view_func=adminAddCourseView, methods=['GET',])
    app.add_url_rule('/admin/createcourse/', view_func=adminAddCourseView, methods=['POST',])

    adminCoursesView = adminCoursesView.as_view('adminCoursesView', database = db)
    app.add_url_rule('/admin/courses/', view_func=adminCoursesView, methods=['GET',])
    

    adminCreateGroupView = adminCreateGroupView.as_view('adminCreateGroupView', database = db)
    app.add_url_rule('/admin/creategroup/', view_func=adminCreateGroupView, methods=['GET',])
    app.add_url_rule('/admin/creategroup/', view_func=adminCreateGroupView, methods=['POST',])

    teacherView = TeacherView.as_view('teacher_view', database = db)
    app.add_url_rule('/teacher/', view_func=teacherView, methods=['GET',])

    logoutView = Logout.as_view("logout_view")
    app.add_url_rule('/logout/', view_func=logoutView, methods=['GET',])
    app.run(debug=True)