from mysql.connector import connect, ProgrammingError
from models import *

class Database(object):
    def __init__(self, hostName, port,  userName, password, database):
        self.host = hostName
        self.port = port
        self.database = database
        self.user = userName
        self.password = password
        self.connection = self.connect()
        
    #This method establish connection to database. 
    def connect(self):
        connection = connect(
            user=self.user,
            host=self.host,
            password=self.password,
            database=self.database,
            port=self.port,
            )
        return connection
       
#####################################  USER  ###############################################

    #######  CREATE USER  #######

    def createUser(self, user_data):
        cursor = self.connection.cursor()
        insert_query = '''INSERT INTO
                            users(
                                userGId, 
                                firstName, 
                                lastName, 
                                email, 
                                pass, 
                                user_type, 
                                active) 
                            VALUES(%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(
            insert_query,
            (user_data.userGId,
             user_data.firstName,
             user_data.lastName,
             user_data.email,
             user_data.password,
             user_data.user_type,
             1))
        self.connection.commit()
        cursor.close()


    #######  UPDATE USER  #######

    def updateUser(self, user_data, email):
        cursor = self.connection.cursor()
        update_query='''UPDATE users
                        SET 
                            firstName=%s,
                            lastName=%s,
                            email=%s,
                            pass=%s,
                            user_type=%s,
                            active=%s
                        WHERE 
                            email=%s'''
        cursor.execute(
            update_query,
            (user_data.firstName,
             user_data.lastName,
             user_data.email,
             user_data.password,
             user_data.user_type,
             user_data.active,
             email))
        self.connection.commit()
        cursor.close()


    #######  GET USER  #######

    def getUser(self, email = '', userGId = ''):
        cursor = self.connection.cursor()
        get_query ='''SELECT userGId,
                    firstName,
                    lastName,
                    email,
                    pass,
                    user_type,
                    active
                  FROM users
                  WHERE
                    email= %s OR userGId = %s'''
        cursor.execute(get_query, (email, userGId,) )
        results = cursor.fetchone()
        if results:
            user = User(
                userGId = results[0],
                firstName = results[1],
                lastName = results[2],
                email = results[3],
                password = results[4],
                user_type = results[5],
                active = results[6])

            cursor.close()
            return user
        cursor.close()
        return None


    #######  GET USERS  #######

    def getUsers(self, user_type, limit=10, index=0):
            cursor = self.connection.cursor()
            query ='''SELECT 
                        userGId,
                        firstName,
                        lastName,
                        email,
                        pass,
                        user_type,
                        active
                        FROM users WHERE user_type=%s AND active=1 LIMIT %s OFFSET %s '''
            cursor.execute(query, (user_type, limit, index))
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
                cursor.close()
                return tab
            else:
                cursor.close()
                return None


    #######  DELETE USER  #######

    def deleteUser(self, email):
        cursor = self.connection.cursor()
        delete_query='''DELETE FROM
                            users
                        WHERE 
                            email=%s'''
        cursor.execute(
            delete_query,
            (email,))
        self.connection.commit()
        cursor.close()

####################################  COURSE  ##############################################


    ######### CREATE COURSE ########

    def createCourse(self, course_data):
        cursor = self.connection.cursor()
        insert_query = "INSERT INTO subjects(name, description) VALUES(%s,%s)"
        cursor.execute(insert_query,(course_data.name,course_data.description))
        self.connection.commit()
        cursor.close()


    ######### GET COURSES ########

    def getCourses(self, limit = 10, index = 0):
        cursor = self.connection.cursor()
        get_query = "SELECT subjectId, name,description FROM subjects LIMIT %s OFFSET %s"
        cursor.execute(get_query,(limit, index))
        courses= cursor.fetchall()
        if courses:
            tab = []
            for course in courses:
                c = Course(subjectId = course[0], name = course[1], description = course[2])
                tab.append(c)
            cursor.close()
            return tab
        else:
            cursor.close()
            return None


    #######  DELETE COURSE  #######

    def deleteCourse(self, courseId):
        cursor = self.connection.cursor()
        delete_query='''DELETE FROM
                            courses
                        WHERE 
                            courseId=%s'''
        cursor.execute(
            delete_query,
            (courseId,))
        self.connection.commit()
        cursor.close()

####################################   GROUP   #########################################

    ######### CREATE GROUP ########
 
    def createGroup(self, group_data):
        cursor = self.connection.cursor()
        insert_query = '''INSERT INTO groups
                            (active,
                            subjectId,
                            teacherId)
                          VALUES(%s,%s,%s)'''
        cursor.execute(insert_query,
            (group_data.active, 
             group_data.subjectId, 
             group_data.teacherId))
            
        self.connection.commit()
        cursor.close()
  
    
    ######## UPDATE GROUP ########

    def updateGroup(self, group_data, groupId):
        cursor = self.connection.cursor()
        update_query='''UPDATE groups
                        SET
                            active=%s,
                            subjectId=%s,
                            teacherId=%s
                        WHERE groupId = %s'''
        cursor.execute(
             update_query,
            (group_data.active,
             group_data.subjectId,
             group_data.teacherId,
             groupId,))

        self.connection.commit()
        cursor.close()

    
    ######## GET GROUPS ########

    def getGroups(self, subjectId, limit = 10, index = 0):
        cursor = self.connection.cursor()
        get_query='''SELECT groupId,
                    subjectId,
                    teacherId
                    FROM groups WHERE subjectId= %s AND active=1 LIMIT %s OFFSET %s'''
        cursor.execute(get_query, (subjectId, limit, index) )          
        groups = cursor.fetchall()
        if groups:
            tab = []
            for group in groups:
                g = Group(
                        groupId = group[0],
                        subjectId = group[1],
                        teacherId = group[2])
                tab.append(g)
            cursor.close()
            return tab
        else:
            cursor.close()
            return None

        #######  DELETE GROUP  #######

    def deleteGroup(self, groupId):
        cursor = self.connection.cursor()
        delete_query='''DELETE FROM
                            groups
                        WHERE 
                            groupId=%s'''
        cursor.execute(
            delete_query,
            (groupId,))
        self.connection.commit()
        cursor.close()


######################################### LESSON ####################################

    ########## GET LESSONS ##########

    def getLessons(self, groupId, limit = 5, index = 0):
        cursor = self.connection.cursor()
        get_query='''SELECT groupId,
                    classroom,
                    dateValue,
                    timeValue
                    FROM lessons WHERE groupId= %s LIMIT %s OFFSET %s'''
        cursor.execute(get_query, (groupId, limit, index))        
        lessons = cursor.fetchall()
        if lessons:
            tab = []
            for lesson in lessons:
                l = Lesson(
                        groupId = lesson[0],
                        classroom = lesson[1],
                        dateValue = lesson[2],
                        timeValue = lesson[3])
                tab.append(l)
            cursor.close()
            return tab
        else:
            cursor.close()
            return None   