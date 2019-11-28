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
    def add_admin(self, email):
        cnx = self.connect()
        cursor = cnx.cursor()
        get_user_promoted_query="UPDATE users SET user_type=admin WHERE email = %s"
        cursor.execute(get_user_promoted_query, (email,))
        cnx.commit()
        cnx.close()

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


    def add_group(self, groupId=None, active=True):
        cnx = self.connect()
        cursor = cnx.cursor()
        insert_query="INSERT INTO groups(active) VALUES(%s)"
        cursor.execute(insert_query, (active,))
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

