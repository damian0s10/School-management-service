from flask import Flask
import logging
import os

hostName = os.getenv("hostName")
port = os.getenv("port")
userName = os.getenv("userName")
password = os.getenv("password")
database = os.getenv("database")

if __name__ == '__main__':
    app = Flask(__name__)
    import unauthviews
    import adminviews
    import teacherviews
    import studentviews
    from database import Database

    app.secret_key = os.urandom(24)
    app.logger = logging.StreamHandler()

    db = Database(hostName=hostName,
                  port=port,
                  userName=userName,
                  password=password,
                  database=database)

    indexView = unauthviews.IndexView.as_view('index_view')
    app.add_url_rule('/', view_func=indexView, methods=['GET',])

    loginView = unauthviews.LoginView.as_view('login_view', database=db)
    app.add_url_rule('/login/', view_func=loginView,methods=['GET',])
    app.add_url_rule('/login/', view_func=loginView, methods=['POST',])

    registerView = unauthviews.RegisterView.as_view('register_view', database=db)
    app.add_url_rule('/register/', view_func=registerView, methods=['GET',])
    app.add_url_rule('/register/', view_func=registerView, methods=['POST',])

    adminView = adminviews.AdminView.as_view('admin_view', database = db)
    app.add_url_rule('/admin/', view_func=adminView, methods=['GET',])

    adminUsersView = adminviews.AdminUsersView.as_view('adminUsers_view', database = db)
    app.add_url_rule('/admin/users_management/', view_func=adminUsersView, methods=['GET',])
    app.add_url_rule('/admin/users_management/', view_func=adminUsersView, methods=['POST',])

    adminAddCourseView = adminviews.AdminAddCourseView.as_view('adminAddCourseView', database = db)
    app.add_url_rule('/admin/createcourse/', view_func=adminAddCourseView, methods=['GET',])
    app.add_url_rule('/admin/createcourse/', view_func=adminAddCourseView, methods=['POST',])

    adminCoursesView = adminviews.AdminCoursesView.as_view('adminCoursesView', database = db)
    app.add_url_rule('/admin/courses/', view_func=adminCoursesView, methods=['GET',])

    adminCreateGroupView = adminviews.AdminCreateGroupView.as_view('adminCreateGroupView', database = db)
    app.add_url_rule('/admin/creategroup/', view_func=adminCreateGroupView, methods=['GET',])
    app.add_url_rule('/admin/creategroup/', view_func=adminCreateGroupView, methods=['POST',])

    adminCreateLessonsView = adminviews.AdminCreateLessonsView.as_view('adminCreateLessonsView', database = db)
    app.add_url_rule('/admin/createlessons/', view_func=adminCreateLessonsView, methods=['GET',])
    app.add_url_rule('/admin/createlessons/', view_func=adminCreateLessonsView, methods=['POST',])

    studentCoursesView = studentviews.StudentCoursesView.as_view('studentCoursesView', database = db)
    app.add_url_rule('/student/courses/', view_func=studentCoursesView, methods=['GET',])
    app.add_url_rule('/student/courses/', view_func=studentCoursesView, methods=['POST',])

    studentGroupsView = studentviews.StudentGroupsView.as_view('studentGroupsView', database = db)
    app.add_url_rule('/student/courses/<subjectId>', view_func=studentGroupsView, methods=['GET',])

    studentView = studentviews.StudentView.as_view('student_view', database = db)
    app.add_url_rule('/student/', view_func=studentView, methods=['GET',])

    studentLessonsView = studentviews.StudentLessonsView.as_view('studentLessonsView', database = db)
    app.add_url_rule('/student/courses/lessons<groupId>', view_func=studentLessonsView, methods=['GET',])
    app.add_url_rule('/student/courses/lessons<groupId>', view_func=studentLessonsView, methods=['POST',])

    studentNewsView = studentviews.StudentNewsView.as_view('studentNewsView', database = db)
    app.add_url_rule('/student/news', view_func=studentNewsView, methods=['GET',])
    
    studentMessageView = studentviews.StudentMessage.as_view('studentMessage', database = db)
    app.add_url_rule('/student/message/<messageId>', view_func=studentMessageView, methods=['GET',])
    
    studentPlanView = studentviews.StudentPlanView.as_view('studentPlanView', database = db)
    app.add_url_rule('/student/plan/<week>', view_func=studentPlanView, methods=['GET',])
    
    teacherView = teacherviews.TeacherView.as_view('teacher_view', database = db)
    app.add_url_rule('/teacher/', view_func=teacherView, methods=['GET',])

    teacherGroupsView = teacherviews.TeacherGroupsView.as_view('teacherGroupsView', database = db)
    app.add_url_rule('/teacher/groups/', view_func=teacherGroupsView, methods=['GET',])

    teacherLessonsView = teacherviews.TeacherLessonsView.as_view('teacherLessonsView', database = db)
    app.add_url_rule('/teacher/groups/lessons/<groupId>', view_func=teacherLessonsView, methods=['GET',])

    teacherAttendancesListView = teacherviews.TeacherAttendanceListView.as_view('teacherAttendancesListView', database = db)
    app.add_url_rule('/teacher/groups/lessons/attendances/<lessonId>', view_func=teacherAttendancesListView, methods=["GET",])
    app.add_url_rule('/teacher/lessons/attendances/', view_func=teacherAttendancesListView, methods=["POST",])

    teacherCreateMessageView = teacherviews.TeacherCreateMessageView.as_view('teacherCreateMessageView', database = db)
    app.add_url_rule('/message/', view_func=teacherCreateMessageView, methods=['GET',])
    app.add_url_rule('/message/', view_func=teacherCreateMessageView, methods=['POST',])

    logoutView = adminviews.Logout.as_view("logout_view")
    app.add_url_rule('/logout/', view_func=logoutView, methods=['GET',])

    app.run()