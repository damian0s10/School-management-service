import flask 
from flask import request, session, render_template, g, redirect
import models 
import logging
from adminviews import UserView
from datetime import datetime, timedelta


class TeacherView(UserView):
    def get(self):
        if self.permission == "teacher":
            return render_template("teacher_view.html",firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")


class TeacherCreateMessageView(UserView):
    def get(self,template="teacher_create_message.html"):
        if self.permission == "teacher":
            try:
                groups = self.db.getGroups(teacherId = session['userGId'])
                return render_template(template,groups = groups,firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

    def post(self):
        if self.permission == "teacher":
            groupId = request.form.get("groupId", "")
            message = request.form.get("message", "")
            title = request.form.get("title", "")
            author = session["first_name"] + " " + session["last_name"]
            m_date = datetime.now()
            m = models.Message(userGId = session["userGId"],
                               groupId = groupId,
                               message = message,
                               title = title,
                               author = author,
                               date = m_date)
            try:
                self.db.insertMessage(m)
                return flask.redirect("/news")
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

class TeacherGroupsView(UserView):
    def get(self, template="teacher_groups.html"):
        if self.permission != "teacher": return flask.redirect('/')
        userGId = session['userGId']
        try:
            groups = self.db.getGroups(teacherId=userGId)
        except Exception as e:
            print(e)
            logging.exception("Connection to database failed")
            return flask.redirect("/")

        return render_template(template, 
                                groups = groups,
                                firstName=session['first_name'], 
                                lastName=session['last_name'])

class TeacherLessonsView(UserView):
    def get(self, groupId, template="teacher_lessons_list.html"):
        if self.permission !="teacher": return flask.redirect('/')
        now = datetime.now()
        date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)
        format =  '%Y-%m-%d'
        date_start = datetime.strptime(date, format)
        date_start = str(date_start.year)+'-'+str(date_start.month)+'-'+str(date_start.day)
        date_stop = datetime.strptime(date, format) + timedelta(days=60)
        date_stop = str(date_stop.year)+'-'+str(date_stop.month)+'-'+str(date_stop.day)
        try:
            lessons = self.db.getLessons(groupId = groupId, date_start = date_start, date_stop = date_stop)
            return render_template(template, lessons = lessons,firstName=session['first_name'], lastName=session['last_name'])
        except Exception as e:
            print(e)
            logging.exception("Connection to database failed")
            return flask.redirect("/")

class TeacherAttendanceListView(UserView):
    def get(self, lessonId, template="teacher_attendance_list.html"):
        if self.permission != "teacher": return flask.redirect("/")
        try:
            lesson = self.db.getLesson(lessonId=lessonId)
            matches = self.db.getMatches(groupId=lesson.groupId)
            students = []
            present = []

            for match in matches:
                student = self.db.getUser(userGId=match.studentId)
                students.append(student)
                a = self.db.getAttendance(lessonId=lessonId, studentId=student.userGId)
                if a.attendance == 1:
                    present.append(a.studentId)

        except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
                return flask.redirect("/")
        return render_template(
                            template,
                            lessonId=lessonId,
                            present = present,
                            students = students,
                            firstName=session['first_name'], 
                            lastName=session['last_name'])

    def post(self):
        if self.permission != "teacher": return flask.redirect("/")
        lessonId = request.form.get("lessonId", '')
        try:
            lesson = self.db.getLesson(lessonId=lessonId)
            matches = self.db.getMatches(groupId=lesson.groupId)
            students = []
            for match in matches:
                student = self.db.getUser(userGId=match.studentId)
                students.append(student)
        except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
                return flask.redirect("/")

        present = []
        for key in request.form: 
            present.append(key)

        for student in students:
            if student.userGId in present: presence = 1
            else: presence = 0

            a = models.Attendance(
                                  lessonId = lessonId,
                                  studentId = key,
                                  attendance = presence)
            try:
                self.db.updateAttendance(attendance_data=a, 
                                         lessonId=lessonId, 
                                         studentId=student.userGId)

            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
                return flask.redirect("/")
            
        return flask.redirect("/teacher/groups/lessons/attendances/"+lessonId)

