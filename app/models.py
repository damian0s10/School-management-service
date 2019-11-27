class User(object):
    def __init__(self, userGId, firstName, lastName, email, password, active, userId = None, user_type="student"):
        self.userId = userId
        self.userGId = userGId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.user_type = user_type
        self.active = True
    
            
class Group(object):
    def __init__(self, groupId=None, active=True):
        self.groupId = groupId
        self.active = active

class Match(object):
    def __init__(self, groupId, studentId, matchId=None):
        self.groupId = groupId
        self.studentId = studentId
        self.matchId = matchId




