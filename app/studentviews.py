import flask 
from flask import request, session, render_template, g, redirect
import models 
import logging
from adminviews import UserView
from datetime import datetime, timedelta


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

class StudentMyGroupsView(UserView):
    def get(self):
        if self.permission != "student": return flask.redirect('/')
        studentGId = session["userGId"]
        try:
            groups = self.db.getMatches(studentId=studentGId)
            if not groups: 
                return render_template("student_statement.html", text = "Nie zapisałeś się do żadnej grupy",firstName=session['first_name'], lastName=session['last_name'] )
            courses_list = []
            for group in groups:
                courses_list.append(self.db.getGroups(groupId = group.groupId))
            if courses_list: 
                return render_template("student_my_groups.html",courses = courses_list, firstName=session['first_name'], lastName=session['last_name'])
                
        except Exception as e:
            print(e)
            logging.exception("ERROR")    
        return flask.redirect("/")
class StudentLessonsView(UserView):
    def get(self, groupId, template="student_lessons.html"):
        if self.permission == "student":
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

    def post(self, groupId, template="student_added_to_group.html"):
        if self.permission == "student":
            userGId = session["userGId"]
            groupId = request.form.get("groupId", "")
            if(self.db.checkMatch(groupId = groupId, studentId = userGId)):
                match = models.Match(groupId = groupId, studentId = userGId, active = 0)
                try:
                    self.db.insertMatch(match)
                    return render_template(template,firstName=session['first_name'], lastName=session['last_name'])
                except Exception as e:
                    print(e)
                    logging.exception("Connection to database failed") 
            return render_template("student_statement.html", text = "Jestes już zapisany do tej grupy",firstName=session['first_name'], lastName=session['last_name'] )   
        return flask.redirect("/")

class StudentNewsView(UserView):
    def get(self, template = "news_list.html"):
        if self.permission != "student": return flask.redirect("/")
        groups = []
        try:
            studentGId = session["userGId"]
            matches = self.db.getMatches(studentId=studentGId)
            if not matches: return render_template("student_statement.html", text = "Nie zapisałeś się do żadnej grupy",firstName=session['first_name'], lastName=session['last_name'] )
            for match in matches:
                groups.append(match.groupId)

            lists = []
            for group in groups:
                messages = self.db.getMessages(groupId = group)
                if messages:
                    for message in messages:
                        lists.append(message)
            if not lists:
                return render_template("student_statement.html", text = "Nie masz żadnych wiadomości",firstName=session['first_name'], lastName=session['last_name'] )
            lists.sort(key=lambda o: o.date, reverse = True)
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
        if not message: return render_template("student_statement.html", text = "Nie udało się pobrać wiadomości",firstName=session['first_name'], lastName=session['last_name'] )
        return render_template("message_detail.html",
                               message = message,
                               firstName=session['first_name'],
                               lastName=session['last_name'])
        
class StudentPlanView(UserView):
    def get(self, template="student_plan.html",week = 0):
        if self.permission != "student": return flask.redirect('/')
        studentGId = session["userGId"]
        now = datetime.now()
        date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)
        format =  '%Y-%m-%d'
        print(now.weekday())
        date_start = datetime.strptime(date, format) + timedelta(days=7*int(week)-now.weekday())
        date_start = str(date_start.year)+'-'+str(date_start.month)+'-'+str(date_start.day)
        date_stop = datetime.strptime(date, format) + timedelta(days=6+7*int(week)-now.weekday())
        date_stop = str(date_stop.year)+'-'+str(date_stop.month)+'-'+str(date_stop.day)
        days = ["Niedziela", "Poniedziałek" , "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota"]
        try:
            all_lessons = []
            groups = self.db.getMatches(studentId=studentGId)
            for group in groups:
                lessons = self.db.getLessons(groupId = group.groupId, date_start = date_start, date_stop = date_stop)
                if lessons: 
                    for lesson in lessons:
                        lesson.dayOfWeek = days[lesson.dayOfWeek-1]
                    all_lessons.extend(lessons)
        except Exception as e:
            print(e)
            logging.exception("ERROR")    
       
        all_lessons.sort(key=lambda o: o.dateValue)
        return render_template(template, date_start = date_start, date_stop = date_stop, last_week = int(week)-1, next_week= int(week) + 1, lessons = all_lessons, firstName=session['first_name'],lastName=session['last_name'])


class StudentGradesView(UserView):
    def get(self, template = "student_grades.html"):
        if self.permission != "student": return flask.redirect('/')
        studentGId = session["userGId"]
        try:
            matches = self.db.getMatches(studentId = studentGId)
            print(matches)
            if not matches: render_template("student_statement.html", text = "Nie jesteś zapisany do grupy",firstName=session['first_name'], lastName=session['last_name'] )
                
            courses_list = {}
            for match in matches:
                subject = self.db.getGroups(groupId = match.groupId)[0].subject_name
                grades = self.db.getGrades(groupId = match.groupId, studentId = studentGId)
                print(grades)
                if not grades:
                    grades = []
                courses_list[subject] = grades
        except Exception as e:
            print(e)
            logging.exception("ERROR")    
        
        return render_template(template, list = courses_list,
                                        firstName=session['first_name'], 
                                        lastName=session['last_name'])

class StudentGradeDescView(UserView):
    def get(self, gradeId, template="student_grade_desc.html"):
        if self.permission != "student": return flask.redirect('/')
        try:
            grade = self.db.getGrades(gradeId = gradeId)
            return render_template(template,
                                    grade = grade,
                                    firstName=session['first_name'], 
                                    lastName=session['last_name'])
        except Exception as e:
            print(e)
            logging.exception("ERROR")
        return flask.redirect("/")