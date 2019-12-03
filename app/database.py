from mysql.connector import connect, ProgrammingError
from models import *

class Database(object):
    def __init__(self, hostName, port,  userName, password, database):
        self.host = hostName
        self.port = port
        self.database = database
        self.user = userName
        self.password = password
        
#This method establish connection to database. 
    def connect(self):
        cnx = connect(user=self.user,
                      host=self.host,
                      password=self.password,
                      database=self.database,
                      port=self.port,
                      )
        return cnx

#This method adds user to database
    def add_user(self, user_data):
        cnx = self.connect()
        cursor = cnx.cursor()
        insert_query = "INSERT INTO users(userGId,firstName,lastName, email, pass, user_type, active) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert_query,
                      (user_data.userGId,
                       user_data.firstName,
                       user_data.lastName,
                       user_data.email,
                       user_data.password,
                       user_data.user_type,
                       1))
        cnx.commit()
        cnx.close()
#This method adds admin to administrators when name given
    def change_type(self, user_type, email):
        cnx = self.connect()
        cursor = cnx.cursor()
        get_user_promoted_query="UPDATE users SET user_type=%s WHERE email = %s"
        cursor.execute(get_user_promoted_query, (user_type, email,))
        cnx.commit()
        cnx.close()

    def change_activity(self, value, email):
        cnx = self.connect()
        cursor = cnx.cursor()
        query="UPDATE users SET active=%s WHERE email = %s"
        cursor.execute(query, (value, email,))
        cnx.commit()
        cnx.close()

#This method adds course, only admin can use 
    def add_course(self, course_data):
        cnx = self.connect()
        cursor = cnx.cursor()
        insert_query = "INSERT INTO subjects(name, description) VALUES(%s,%s)"
        cursor.execute(insert_query,(course_data.name,course_data.description))
        cnx.commit()
        cnx.close()

#This method adds group, only admin can use 
    def add_group(self, group_data):
        cnx = self.connect()
        cursor = cnx.cursor()
        insert_query = "INSERT INTO groups(active, subjectId, teacherId) VALUES(%s,%s,%s)"
        cursor.execute(insert_query,(group_data.active,group_data.subjectId,group_data.teacherId))
        cnx.commit()
        cnx.close()

#This method gets all courses, only admin can use 
    def get_all_courses(self):
        cnx = self.connect()
        cursor = cnx.cursor()
        query = "SELECT subjectId, name,description FROM subjects "
        cursor.execute(query)
        courses= cursor.fetchall()
        if courses:
            tab = []
            for course in courses:
                c = Course(subjectId = course[0], name = course[1], description = course[2])
                tab.append(c)
            cnx.close()
            return tab
        else:
            cnx.close()
            return None
#This methon gets all teachers, only admin can use
    def get_all_teachers(self):
        cnx = self.connect()
        cursor = cnx.cursor()
        query ='''SELECT 
                    userGId,
                    firstName,
                    lastName,
                    email,
                    pass,
                    user_type,
                    active
                    FROM users WHERE user_type='teacher' AND active = '1' '''
        cursor.execute(query)
        teachers = cursor.fetchall()
        if teachers:
            tab = []
            for teacher in teachers:
                u = User(
                        userGId = teacher[0],
                        firstName = teacher[1],
                        lastName = teacher[2],
                        email = teacher[3],
                        password = teacher[4],
                        user_type = teacher[5],
                        active = teacher[6])
                tab.append(u)
            cnx.close()
            return tab
        else:
            cnx.close()
            return None
    
    
    def get_members_by_type(self, user_type):
            cnx = self.connect()
            cursor = cnx.cursor()
            query ='''SELECT 
                        userGId,
                        firstName,
                        lastName,
                        email,
                        pass,
                        user_type,
                        active
                        FROM users WHERE user_type=%s AND active = 1'''
            cursor.execute(query, (user_type,))
            members = cursor.fetchall()
            if members:
                tab = []
                for member in members:
                    u = User(
                            userGId = member[0],
                            firstName = member[1],
                            lastName = member[2],
                            email = member[3],
                            password = member[4],
                            user_type = member[5],
                            active = member[6])
                    tab.append(u)
                cnx.close()
                return tab
            else:
                cnx.close()
                return None

    '''
    def add_student_to_group(self, groupId, userGId):
        cnx = self.connect()
        cursor = cnx.cursor()
        query = "INSERT INTO matches(groupId, studentId) VALUES(%s,%s)"
        cursor.execute(query, (groupId, studentId,))
        cnx.commit()
        cnx.close()
    '''

    def add_teacher(self, email):
        cnx = self.connect()
        cursor = cnx.cursor()
        query = "UPDATE users SET user_type=teacher WHERE VALUES(%s)"
        cursor.execute(query, (email,))
        cnx.commit()
        cnx.close()


    
#This method returns admin data when email given
 

#This method returns user data when name given
    def get_user_by_email(self,email):
        cnx = self.connect()
        cursor = cnx.cursor()
        query ='''SELECT userGId,
                    firstName,
                    lastName,
                    email,
                    pass,
                    user_type,
                    active
                  FROM users WHERE email= %s'''
        cursor.execute(query, (email,) )
        results = cursor.fetchone()
        if results:
            user = User(userGId = results[0],
                        firstName = results[1],
                        lastName = results[2],
                        email = results[3],
                        password = results[4],
                        user_type = results[5],
                        active = results[6])
            cnx.close()
            return user
        
        cnx.close()
        return None


    def get_user_by_id(self,userGId):
        cnx = self.connect()
        cursor = cnx.cursor()
        query ='''SELECT userGId,
                    firstName,
                    lastName,
                    email,
                    pass,
                    user_type,
                    active
                FROM users WHERE userGId= %s'''
        cursor.execute(query, (userGId,) )
        results = cursor.fetchone()
        if results:
            user = User(userGId = results[0],
                        firstName = results[1],
                        lastName = results[2],
                        email = results[3],
                        password = results[4],
                        user_type = results[5],
                        active = results[5])
            cnx.close()
            return user
        else:
            cnx.close()
            return None

    #def get_students_by_group(self, groupId):
    #    cnx = self.connect()
    #    cursor = cnx.cursor()
    #    query = '''SELECT 
    #                users.firstName,
    #                users.lastName,
    #                users.email,
    #                users.pass,
    #                users.active,
    #                students.userId,
    #                students.studentId
    #                FROM users INNER JOIN students ON students.userId=users.userId
    #                INNER JOIN matches ON students.studentId=matches.studentId
    #                WHERE groupId = %s'''
    #    cursor.execute(query, (groupId,))
    #    students = cursor.fetchall()
    #    if(students):
    #        tab = []
    #        for student in students:
    #            stud = Student(firstName = student[0],
    #                           lastName = student[1],
    #                           email = student[2],
    #                           password = student[3],
    #                           active = student[4],
    #                           studentId = student[5],
    #                           userId = student[6])
    #            tab.append(stud)
    #        cnx.close()
    #        return tab
    #    else:
    #        cnx.close()
    #        return None


    def close_group(self, groupId):
        cnx = self.connect()
        cursor = cnx.cursor()
        insert_query="UPDATE groups SET active = %s WHERE groupId = %s "
        cursor.execute(insert_query, (False, groupId,))
        cnx.commit()
        cnx.close()

