class User(object):
    def __init__(self, userGId, firstName, lastName, email, password, active, user_type="student"):
        self.userGId = userGId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.user_type = user_type
        self.active = True
    
class Group(object):
    def __init__(self, subjectId, teacherId, groupId=None, active=True):
        self.groupId = groupId
        self.active = active
        self.subjectId = subjectId
        self.teacherId = teacherId

class Match(object):
    def __init__(self, groupId, studentId, matchId=None):
        self.groupId = groupId
        self.studentId = studentId
        self.matchId = matchId

class Course(object):
    def __init__(self, name,description, subjectId=None):
        self.name = name
        self.description = description
        self.subjectId = subjectId


