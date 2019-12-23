import flask 
from flask import request, session, render_template, g, redirect
import models 
import logging
from adminviews import UserView


class StudentView(UserView):
    def get(self):
        if self.permission == "student":
            return render_template("student_view.html",firstName=session['first_name'], lastName=session['last_name'])
        return flask.redirect("/")

class StudentCoursesView(UserView):
    def get(self):
        if self.permission == "student":
            try:
                courses = self.db.getCourses()
                return render_template("student_courses.html",courses=courses, firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

class StudentGroupsView(UserView):
    def get(self, subjectId):
        if self.permission == "student":
            try:
                groups = self.db.getGroups(subjectId)
                for group in groups:
                    teacher = self.db.getUser(userGId=group.teacherId)
                    group.teacherId = teacher.firstName + ' ' + teacher.lastName
                return render_template("student_groups.html", groups = groups,firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

class StudentLessonsView(UserView):
    def get(self, groupId, template="student_lessons.html"):
        if self.permission == "student":
            try:
                lessons = self.db.getLessons(groupId)
                return render_template(template, lessons = lessons,firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")

    def post(self, groupId, template="student_added_to_group.html"):
        if self.permission == "student":
            userGId = session["userGId"]
            groupId = request.form.get("groupId", "")
            match = models.Match(groupId = groupId, studentId = userGId, active = 1)
            try:
                self.db.insertMatch(match)
                return render_template(template,firstName=session['first_name'], lastName=session['last_name'])
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")    
        return flask.redirect("/")

class StudentNewsView(UserView):
    def get(self, template = "news_list.html"):
        if self.permission != "student": return flask.redirect("/")
        groups = []
        try:
            studentGId = session["userGId"]
            matches = self.db.getMatches(studentId=studentGId)

            if not matches: return "Nie zapisałeś się do żadnej grupy"
            for match in matches:
                groups.append(match.groupId)

            lists = []
            for i in range(len(groups)-1):
                lists.append(self.db.getMessages(groupId = groups[i]))

            if not lists:
                return "Nie masz żadnych wiadomości od prowadzących"
        except Exception as e:
            print(e)
            logging.exception("ERROR")

        return render_template(template,
                               lists = lists,
                               firstName=session['first_name'],
                               lastName=session['last_name'])
                               
    
class StudentMessage(UserView):
    def get(self, messageId, template = "message_detail.hmtl"):
        if self.permission != "student": return flask.redirect('/')
        try:
            message = self.db.getMessage(messageId = messageId)
        except Exception as e:
            print(e)
            logging.exception("ERROR")
        if not message: return "Nie udało się pobrać wiadomości"
        return render_template("message_detail.html",
                               message = message,
                               firstName=session['first_name'],
                               lastName=session['last_name'])
        

