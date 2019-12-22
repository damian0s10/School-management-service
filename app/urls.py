from flask import Blueprint
import unauthviews 
import adminviews 
import teacherviews
import studentviews
from database import db

apps = Blueprint('apps', __name__)

indexView = unauthviews.IndexView.as_view('index_view')
apps.add_url_rule('/', view_func=indexView, methods=['GET',])

loginView = unauthviews.LoginView.as_view('login_view', database=db)
apps.add_url_rule('/login/', view_func=loginView,methods=['GET',])
apps.add_url_rule('/login/', view_func=loginView, methods=['POST',])

registerView = unauthviews.RegisterView.as_view('register_view', database=db)
apps.add_url_rule('/register/', view_func=registerView, methods=['GET',])
apps.add_url_rule('/register/', view_func=registerView, methods=['POST',])

adminView = adminviews.AdminView.as_view('admin_view', database = db)
apps.add_url_rule('/admin/', view_func=adminView, methods=['GET',])

adminUsersView = adminviews.AdminUsersView.as_view('adminUsers_view', database = db)
apps.add_url_rule('/admin/users_management/', view_func=adminUsersView, methods=['GET',])
apps.add_url_rule('/admin/users_management/', view_func=adminUsersView, methods=['POST',])

adminAddCourseView = adminviews.AdminAddCourseView.as_view('adminAddCourseView', database = db)
apps.add_url_rule('/admin/createcourse/', view_func=adminAddCourseView, methods=['GET',])
apps.add_url_rule('/admin/createcourse/', view_func=adminAddCourseView, methods=['POST',])

adminCoursesView = adminviews.AdminCoursesView.as_view('adminCoursesView', database = db)
apps.add_url_rule('/admin/courses/', view_func=adminCoursesView, methods=['GET',])

adminCreateGroupView = adminviews.AdminCreateGroupView.as_view('adminCreateGroupView', database = db)
apps.add_url_rule('/admin/creategroup/', view_func=adminCreateGroupView, methods=['GET',])
apps.add_url_rule('/admin/creategroup/', view_func=adminCreateGroupView, methods=['POST',])

studentCoursesView = studentviews.StudentCoursesView.as_view('studentCoursesView', database = db)
apps.add_url_rule('/student/courses/', view_func=studentCoursesView, methods=['GET',])
apps.add_url_rule('/student/courses/', view_func=studentCoursesView, methods=['POST',])

studentGroupsView = studentviews.StudentGroupsView.as_view('studentGroupsView', database = db)
apps.add_url_rule('/student/courses/<subjectId>', view_func=studentGroupsView, methods=['GET',])

studentView = studentviews.StudentView.as_view('student_view', database = db)
apps.add_url_rule('/student/', view_func=studentView, methods=['GET',])

studentLessonsView = studentviews.StudentLessonsView.as_view('studentLessonsView', database = db)
apps.add_url_rule('/student/courses/lessons<groupId>', view_func=studentLessonsView, methods=['GET',])
apps.add_url_rule('/student/courses/lessons<groupId>', view_func=studentLessonsView, methods=['POST',])

teacherView = teacherviews.TeacherView.as_view('teacher_view', database = db)
apps.add_url_rule('/teacher/', view_func=teacherView, methods=['GET',])

teacherCreateMessageView = teacherviews.TeacherCreateMessageView.as_view('teacherCreateMessageView', database = db)
apps.add_url_rule('/message/', view_func=teacherCreateMessageView, methods=['GET',])
apps.add_url_rule('/message/', view_func=teacherCreateMessageView, methods=['POST',])

logoutView = adminviews.Logout.as_view("logout_view")
apps.add_url_rule('/logout/', view_func=logoutView, methods=['GET',])