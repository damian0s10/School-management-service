from flask import Blueprint
from config import hostName, port, userName, password, database
from database import Database

db = Database(hostName=hostName,
                 port=port,
                 userName=userName,
                 password=password,
                 database=database)

teacher_bp = Blueprint('teacher', __name__,
                       template_folder='templates')

from teacher.views import *

teacherView = TeacherView.as_view('teacher_view', database = db)

teacher_bp.add_url_rule('/teacher/', view_func=teacherView, methods=['GET',])

teacherCreateMessageView = TeacherCreateMessageView.as_view('teacherCreateMessageView', database = db)

teacher_bp.add_url_rule('/message/', view_func=teacherCreateMessageView, methods=['GET',])
teacher_bp.add_url_rule('/message/', view_func=teacherCreateMessageView, methods=['POST',])