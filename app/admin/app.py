from flask import Blueprint
from config import hostName, port, userName, password, database
from database import Database

db = Database(hostName=hostName,
                 port=port,
                 userName=userName,
                 password=password,
                 database=database)

admin_bp = Blueprint('admin', __name__,
                  template_folder='templates')
                  
from admin.views import *

adminView = AdminView.as_view('admin_view', database = db)
admin_bp.add_url_rule('/admin/', view_func=adminView, methods=['GET',])

adminUsersView = AdminUsersView.as_view('adminUsers_view', database = db)
admin_bp.add_url_rule('/admin/users_management/', view_func=adminUsersView, methods=['GET',])
admin_bp.add_url_rule('/admin/users_management/', view_func=adminUsersView, methods=['POST',])

adminAddCourseView = AdminAddCourseView.as_view('adminAddCourseView', database = db)
admin_bp.add_url_rule('/admin/createcourse/', view_func=adminAddCourseView, methods=['GET',])
admin_bp.add_url_rule('/admin/createcourse/', view_func=adminAddCourseView, methods=['POST',])

adminCoursesView = AdminCoursesView.as_view('adminCoursesView', database = db)
admin_bp.add_url_rule('/admin/courses/', view_func=adminCoursesView, methods=['GET',])
    
adminCreateGroupView = AdminCreateGroupView.as_view('adminCreateGroupView', database = db)
admin_bp.add_url_rule('/admin/creategroup/', view_func=adminCreateGroupView, methods=['GET',])
admin_bp.add_url_rule('/admin/creategroup/', view_func=adminCreateGroupView, methods=['POST',])
