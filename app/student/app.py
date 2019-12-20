from flask import Blueprint
from config import hostName, port, userName, password, database
from database import Database

db = Database(hostName=hostName,
                 port=port,
                 userName=userName,
                 password=password,
                 database=database)

student_bp = Blueprint('student', __name__,
                       template_folder='templates')

from student.views import *

studentView = StudentView.as_view('student_view', database = db)
student_bp.add_url_rule('/student/', view_func=studentView, methods=['GET',])

studentCoursesView = StudentCoursesView.as_view('studentCoursesView', database = db)
student_bp.add_url_rule('/student/courses/', view_func=studentCoursesView, methods=['GET',])
student_bp.add_url_rule('/student/courses/', view_func=studentCoursesView, methods=['POST',])

studentGroupsView = StudentGroupsView.as_view('studentGroupsView', database = db)
student_bp.add_url_rule('/student/courses/<subjectId>', view_func=studentGroupsView, methods=['GET',])

studentLessonsView = StudentLessonsView.as_view('studentLessonsView', database = db)
student_bp.add_url_rule('/student/courses/lessons<groupId>', view_func=studentLessonsView, methods=['GET',])
student_bp.add_url_rule('/student/courses/lessons<groupId>', view_func=studentLessonsView, methods=['POST',])