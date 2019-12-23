from mysql.connector import connect, ProgrammingError
import models

class Database(object):
    def __init__(self, hostName, port,  userName, password, database):
        self.connection = self.connect(hostName, port,  userName, password, database)
        
    #This method establish connection to database. 
    def connect(self, hostName, port,  userName, password, database):
        return connect(
            user=userName,
            host=hostName,
            password=password,
            database=database,
            port=port,
            )
       
#####################################  USER  ###############################################

    def insertUser(self, user_data):
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
            user = models.User(
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
                        FROM
                            users 
                        WHERE user_type=%s AND active=1
                        LIMIT %s OFFSET %s; '''

                        
            cursor.execute(query, (user_type, limit, index))
            members = cursor.fetchall()

            if not members:
                cursor.close()
                return None
            tab = []
            for member in members:
                u = models.User(
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
                


    def deleteUser(self, email):
        cursor = self.connection.cursor()
        delete_query="DELETE FROM users WHERE email=%s"
        cursor.execute(
            delete_query,
            (email,))
        self.connection.commit()
        cursor.close()

####################################  COURSE  ##############################################


    def insertCourse(self, course_data):
        cursor = self.connection.cursor()
        insert_query = "INSERT INTO subjects(name, description) VALUES(%s,%s)"
        cursor.execute(insert_query,(course_data.name,course_data.description))
        self.connection.commit()
        cursor.close()



    def getCourses(self, limit = 10, index = 0):
        cursor = self.connection.cursor()
        get_query = "SELECT subjectId, name,description FROM subjects LIMIT %s OFFSET %s"
        cursor.execute(get_query,(limit, index))
        courses= cursor.fetchall()
        if not courses:
            cursor.close()
            return None
        tab = []
        for course in courses:
            c = models.Course(subjectId = course[0], name = course[1], description = course[2])
            tab.append(c)
        cursor.close()
        return tab



    def deleteCourse(self, courseId):
        cursor = self.connection.cursor()
        delete_query="DELETE FROM courses WHERE courseId=%s"
        cursor.execute(
            delete_query,
            (courseId,))
        self.connection.commit()
        cursor.close()

####################################   GROUP   #########################################

 
    def insertGroup(self, group_data):
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

    

    def getGroups(self, subjectId = '', teacherId = '', all = 0, limit = 10, index = 0):
        cursor = self.connection.cursor()
        get_query='''SELECT groupId,
                    subjectId,
                    teacherId
                    FROM groups WHERE (subjectId = %s OR teacherId = %s OR active = %s) AND active=1 LIMIT %s OFFSET %s'''
        cursor.execute(get_query, (subjectId, teacherId, all, limit, index) )          
        groups = cursor.fetchall()
        
        if not groups:
            cursor.close()
            return None 
        tab = []
        for group in groups:
            g = models.Group(
                    groupId = group[0],
                    subjectId = group[1],
                    teacherId = group[2])
            tab.append(g)
        cursor.close()
        return tab
            


    def deleteGroup(self, groupId):
        cursor = self.connection.cursor()
        delete_query="DELETE FROM groups WHERE groupId=%s"
        cursor.execute(
            delete_query,
            (groupId,))
        self.connection.commit()
        cursor.close()


######################################### LESSON ####################################


    def getLessons(self, groupId, limit = 5, index = 0):
        cursor = self.connection.cursor()
        get_query='''SELECT groupId,
                    classroom,
                    dateValue,
                    timeValue
                    FROM lessons WHERE groupId= %s LIMIT %s OFFSET %s'''
        cursor.execute(get_query, (groupId, limit, index))        
        lessons = cursor.fetchall()
        
        if not lessons:
            cursor.close()
            return None  
        tab = []
        for lesson in lessons:
            l = models.Lesson(
                    groupId = lesson[0],
                    classroom = lesson[1],
                    dateValue = lesson[2],
                    timeValue = lesson[3])
            tab.append(l)
        cursor.close()
        return tab 

    def insertLesson(self, lesson_data):
        cursor = self.connection.cursor()
        insert_query="INSERT INTO lessons (groupId, classroom, dateValue, timeValue) VALUES (%s,%s,%s,%s)"
        cursor.execute(insert_query, (lesson_data.groupId, lesson_data.classroom, lesson_data.dateValue, lesson_data.timeValue))
        self.connection.commit()
        cursor.close()

########################## Matches ################################

    def insertMatch(self, match_data):
        cursor = self.connection.cursor()
        insert_query="INSERT INTO matches (groupId, studentId, active) VALUES (%s,%s,%s)"
        cursor.execute(insert_query, (match_data.groupId, match_data.studentId, match_data.active))
        self.connection.commit()
        cursor.close()

    def getMatches(self, groupId='', studentId='', active='', limit=10, index=0):
        cursor = self.connection.cursor()
        get_query='''SELECT groupId,
                            studentId,
                            matchId,
                            active
                    FROM matches
                    WHERE (groupId= %s OR studentId= %s OR active= %s)
                    LIMIT %s OFFSET %s 
                 '''
        cursor.execute(get_query, (groupId,
                                   studentId,
                                   active,
                                   limit,
                                   index))
        matches = cursor.fetchall()
        if not matches:
            cursor.close()
            return None
        match_list = []
        for match in matches:
            m = models.Match(
                             groupId = match[0],
                             studentId = match[1],
                             matchId = match[2],
                             active = match[3])
            match_list.append(m)
        cursor.close()
        return match_list
        

            
        
        


########################## Message #################

    def insertMessage(self, message_data):
        cursor = self.connection.cursor()
        insert_query='''INSERT INTO messages(userGId,
                                             groupId,
                                             message,
                                             title,
                                             date,
                                             author) 
                                        VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(insert_query, (message_data.userGId,
                                      message_data.groupId,
                                      message_data.message,
                                      message_data.title,
                                      message_data.date,
                                      message_data.author))
        self.connection.commit()
        cursor.close()


    def getMessage(self, messageId):
        cursor = self.connection.cursor()
        get_query = ''' SELECT 
                             userGId,
                             author,
                             title,
                             groupId,   
                             message,
                             date 
                        FROM messages
                        WHERE messageId = %s'''
        cursor.execute(get_query, (messageId,))
        result = cursor.fetchone()
        if not result: 
            cursor.close()
            return None

        message = models.Message(userGId=result[0],
                                 author=result[1],
                                 title=result[2],
                                 groupId=result[3],
                                 message=result[4],
                                 date=result[5])
        cursor.close()
        return message
        

        


    def getMessages(self, groupId = '', userGId = '', limit = 10, index = 0):
        cursor = self.connection.cursor()
        get_query ='''SELECT 
                            userGId,
                            author,
                            title,
                            groupId,
                            message,
                            date,
                            messageId
                        FROM messages
                        WHERE (groupId=%s OR userGId=%s)
                        LIMIT %s OFFSET %s 
                 '''
        cursor.execute(get_query,
                      (groupId,
                       userGId,
                       limit,
                       index))
        messages = cursor.fetchall()
        if not messages:
            cursor.close()
            return None
        
        m_list = []
        for message in messages:
            m = models.Message(
                               userGId = message[0],
                               author = message[1],
                               title = message[2],
                               groupId = message[3],
                               message = message[4],
                               date = message[5],
                               messageId = message[6])
            m_list.append(m)
        cursor.close()
        return m_list


        
