class User(object):
    def __init__(self, userGId, firstName, lastName, email, password, active=True, user_type="student"):
        self.userGId = userGId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.user_type = user_type
        self.active = active
    
class Group(object):
    def __init__(self, subjectId, teacherId, groupId=None, active=True, subject_name=None):
        self.groupId = groupId
        self.active = active
        self.subjectId = subjectId
        self.teacherId = teacherId
        self.subject_name = subject_name

class Match(object):
    def __init__(self, groupId, studentId, matchId=None,active=True, firstName =None, lastName = None):
        self.groupId = groupId
        self.studentId = studentId
        self.matchId = matchId
        self.active = active
        self.firstName = firstName
        self.lastName = lastName

class Course(object):
    def __init__(self, name,description, subjectId=None):
        self.name = name
        self.description = description
        self.subjectId = subjectId

class Lesson(object):
    def __init__(self, groupId, classroom, dateValue, timeValue, dayOfWeek = None, subject = None, lessonId = None):
        self.groupId = groupId
        self.classroom = classroom
        self.dateValue = dateValue
        self.timeValue = timeValue
        self.dayOfWeek = dayOfWeek
        self.subject = subject
        self.lessonId = lessonId

class Message(object):
    def __init__(self, userGId, groupId, message, title, author, date, messageId=None):
        self.userGId = userGId
        self.groupId = groupId
        self.message = message
        self.title = title
        self.author = author
        self.date = date
        self.messageId = messageId

class Attendance(object):
    def __init__(self, lessonId, studentId, attendance = 0, attendanceId = None):
        self.lessonId = lessonId
        self.studentId = studentId
        self.attendance = attendance
        self.attendanceId = attendanceId

class Grade(object):
    def __init__(self, groupId, studentId, desc, grade,gradeId = None, firstName = None, lastName = None):
        self.groupId = groupId
        self.studentId = studentId
        self.grade = grade
        self.desc = desc
        self.gradeId = gradeId
        self.firstName = firstName
        self.lastName = lastName