class User(object):
    def __init__(self, firstName, lastName, email, password, active, userId = None):
        self.userId = userId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.active = True
    
class Administrator(User):
    def __init__(self, firstName, lastName, email, password, active, adminId=None, userId=None):
        super(Administrator,self).__init__(userId = userId,
                                           firstName = firstName,
                                           lastName = lastName,
                                           email = email,
                                           password = password,
                                           active = active)
        self.adminId = adminId
        
class Teacher(User):
    def __init__(self, firstName, lastName, email, password, active, teacherId=None, userId=None):
        super(Teacher, self).__init__(userId = userId,
                                      firstName = firstName,
                                      lastName = lastName,
                                      email = email,
                                      password = password,
                                      active = active)
        self.teacherId = teacherId

class Student(User):
    def __init__(self, firstName, lastName, email, password, active, studentId=None, userId=None,):
        super(Student, self).__init__(userId = userId,
                                      firstName = firstName,
                                      lastName = lastName,
                                      email = email,
                                      password = password,
                                      active = active)
        self.studentId = studentId

            
class Group(object):
    def __init__(self, groupId=None, active=True):
        self.groupId = groupId
        self.active = active

class Match(object):
    def __init__(self, groupId, studentId, matchId=None):
        self.groupId = groupId
        self.studentId = studentId
        self.matchId = matchId




