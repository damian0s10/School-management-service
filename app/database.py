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
        insert_query = "INSERT INTO users(firstName,lastName, email, pass, active) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(insert_query,
                      (user_data.firstName,
                       user_data.lastName,
                       user_data.email,
                       user_data.password,
                       1))
        cnx.commit()
        cnx.close()
#This method adds admin to administrators when name given
    def add_admin(self, email):
        cnx = self.connect()
        cursor = cnx.cursor()
        get_user_promoted_query="SELECT userId FROM users WHERE email = %s"
        cursor.execute(get_user_promoted_query, (email,))
        promoted_id = cursor.fetchone()
        insert_admin_query = "INSERT INTO administrators(userId) VALUES(%s)"
        cursor.execute(insert_admin_query, (promoted_id[0],))
        cnx.commit()
        cnx.close()

    def add_student(self, userId):
        cnx = self.connect()
        cursor = cnx.cursor()
        query = "INSERT INTO students(userId) VALUES(%s)"
        cursor.execute(query, (userId,))
        cnx.commit()
        cnx.close()

    def add_student_to_group(self, groupId, studentId):
        cnx = self.connect()
        cursor = cnx.cursor()
        query = "INSERT INTO matches(groupId, studentId) VALUES(%s,%s)"
        cursor.execute(query, (groupId, studentId,))
        cnx.commit()
        cnx.close()

    def add_teacher(self, userId):
        cnx = self.connect(self)
        cursor = cnx.cursor()
        query = "INSERT INTO teachers(userId) VALUES(%s)"
        cursor.execute(query, (userId,))
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
    def get_admin_by_email(self, email):
        cnx = self.connect()
        cursor = cnx.cursor()
        get_admin_query = '''SELECT administrators.adminId,
                                    administrators.userId,
                                    users.firstName,
                                    users.lastName,
                                    users.email,
                                    users.pass,
                                    users.active
                             FROM administrators INNER JOIN users
                             ON administrators.userId=users.userId
                             WHERE users.email = %s'''
        cursor.execute(get_admin_query, (email,))
        admin_data = cursor.fetchone()
        if admin_data:
            admin=Administrator(adminId = admin_data[0],
                                userId = admin_data[1],
                                firstName = admin_data[2],
                                lastName = admin_data[3],
                                email = admin_data[4],
                                password = admin_data[5],
                                active = admin_data[6])
            cnx.close()
            return admin
        else:
            cnx.close()
            return None

#This method returns user data when name given
    def get_user_by_email(self,email):
        cnx = self.connect()
        cursor = cnx.cursor()
        query ='''SELECT userId,
                    firstName,
                    lastName,
                    email,
                    pass,
                    active
                  FROM users WHERE email= %s'''
        cursor.execute(query, (email,) )
        results = cursor.fetchone()
        if results:
            user = User(userId = results[0],
                        firstName = results[1],
                        lastName = results[2],
                        email = results[3],
                        password = results[4],
                        active = results[5])
            cnx.close()
            return user
        
        cnx.close()
        return None


    def get_user_by_ident(self,userId):
        cnx = self.connect()
        cursor = cnx.cursor()
        query ='''SELECT userId,
                    firstName,
                    lastName,
                    email,
                    pass,
                    active
                FROM users WHERE userId= %s'''
        cursor.execute(query, (userId,) )
        results = cursor.fetchone()
        if results:
            user = User(userId = results[0],
                        firstName = results[1],
                        lastName = results[2],
                        email = results[3],
                        password = results[4],
                        active = results[5])
            cnx.close()
            return user
        else:
            cnx.close()
            return None

    def get_students_by_group(self, groupId):
        cnx = self.connect()
        cursor = cnx.cursor()
        query = '''SELECT 
                    users.firstName,
                    users.lastName,
                    users.email,
                    users.pass,
                    users.active,
                    students.userId,
                    students.studentId
                    FROM users INNER JOIN students ON students.userId=users.userId
                    INNER JOIN matches ON students.studentId=matches.studentId
                    WHERE groupId = %s'''
        cursor.execute(query, (groupId,))
        students = cursor.fetchall()
        if(students):
            tab = []
            for student in students:
                stud = Student(firstName = student[0],
                               lastName = student[1],
                               email = student[2],
                               password = student[3],
                               active = student[4],
                               studentId = student[5],
                               userId = student[6])
                tab.append(stud)
            cnx.close()
            return tab
        else:
            cnx.close()
            return None

    def get_teacher_by_ident(self, userId):
        cnx = self.connect()
        cursor = cnx.cursor()
        query = '''SELECT users.firstName,
                          users.lastName,
                          users.email,
                          users.password,
                          users.active,
                          users.userId,
                          teachers.teacherId
                          FROM users INNER JOIN teachers
                          ON users.userId=teachers.teacherId 
                          WHERE teachers.userId = %s'''
        cursor.execute(query,(userId,))
        result = cursor.fetchone()
        if result:
            teacher = Teacher(firstName = result[0],
                              lastName = result[1],
                              email = result[2],
                              password = result[3],
                              active = result[4],
                              teacherId = result[6],
                              userId = result[5])
            cnx.close()
            return teacher
        else:
            cnx.close()
            return None

    def close_group(self, groupId):
        cnx = self.connect()
        cursor = cnx.cursor()
        insert_query="UPDATE groups SET active = %s WHERE groupId = %s "
        cursor.execute(insert_query, (False, groupId,))
        cnx.commit()
        cnx.close()