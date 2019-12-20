import flask
from flask import request, session, render_template, g
from models import *
from flask.views import MethodView
import logging
from admin.views import UserView
from teacher.app import db

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
            m = Message(userGId = session["userGId"], groupId = groupId, message = message)
            try:
                self.db.insertMessage(m)
                return flask.redirect("/news")
            except Exception as e:
                print(e)
                logging.exception("Connection to database failed")
        return flask.redirect("/")