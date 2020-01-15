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

    

    def getGroups(self, subjectId = '', teacherId = '', groupId = '', all = 0, limit = 10, index = 0):
        cursor = self.connection.cursor()
        get_query='''SELECT groups.groupId,
                    groups.subjectId,
                    groups.teacherId,
                    subjects.name
                    FROM groups
                    INNER JOIN subjects
                    ON groups.subjectId = subjects.subjectId
                    WHERE (groups.subjectId = %s OR groups.teacherId = %s OR groups.groupId = %s OR groups.active = %s) AND groups.active=1 LIMIT %s OFFSET %s'''
        cursor.execute(get_query, (subjectId, teacherId, groupId, all, limit, index) )          
        groups = cursor.fetchall()
        
        if not groups:
            cursor.close()
            return None 
        tab = []
        for group in groups:
            g = models.Group(
                    groupId = group[0],
                    subjectId = group[1],
                    teacherId = group[2],
                    subject_name = group[3])
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


    def getLessons(self, groupId, date_start = "", date_stop = "", limit = 20, index = 0):
        cursor = self.connection.cursor()
        get_query=''' SELECT 
                    lessons.lessonId,
                    lessons.groupId,
                    lessons.classroom,
                    lessons.dateValue,
                    lessons.timeValue,
                    subjects.name,
                    DAYOFWEEK(lessons.dateValue)
                    FROM ((groups
                    INNER JOIN lessons ON groups.groupId = lessons.groupId)
                    INNER JOIN subjects ON groups.subjectId = subjects.subjectId)
                    WHERE lessons.groupId = %s AND lessons.dateValue BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE) 
                    LIMIT %s OFFSET %s'''

        cursor.execute(get_query, (groupId, date_start, date_stop, limit, index))        
        lessons = cursor.fetchall()
        
        if not lessons:
            cursor.close()
            return None  
        tab = []
        for lesson in lessons:
            l = models.Lesson(
                    lessonId = lesson[0],
                    groupId = lesson[1],
                    classroom = lesson[2],
                    dateValue = lesson[3],
                    timeValue = lesson[4],
                    subject = lesson[5],
                    dayOfWeek = lesson[6])
            tab.append(l)
        cursor.close()
        return tab 

    def insertLesson(self, lesson_data):
        cursor = self.connection.cursor()
        insert_query="INSERT INTO lessons (groupId, classroom, dateValue, timeValue) VALUES (%s,%s,%s,%s)"
        cursor.execute(insert_query, (lesson_data.groupId, lesson_data.classroom, lesson_data.dateValue, lesson_data.timeValue))
        self.connection.commit()
        cursor.close()

    def getLesson(self, groupId='', dateValue='', timeValue='', lessonId=''):
        cursor = self.connection.cursor(buffered = True)
        get_query = '''SELECT
                        lessonId,
                        groupId,
                        classroom, 
                        dateValue, 
                        timeValue
                    FROM lessons WHERE (groupId = %s AND dateValue = %s AND timeValue = %s) OR lessonId = %s'''
        cursor.execute(get_query, (groupId, dateValue, timeValue, lessonId))
        result = cursor.fetchone()
        lesson = models.Lesson(
                                lessonId = result[0],
                                groupId = result[1],
                                classroom = result[2],
                                dateValue = result[3],
                                timeValue = result[4])
        cursor.close()
        return lesson


########################## MATCH ################################

    def insertMatch(self, match_data):
        cursor = self.connection.cursor()
        insert_query="INSERT INTO matches (groupId, studentId, active) VALUES (%s,%s,%s)"
        cursor.execute(insert_query, (match_data.groupId, match_data.studentId, match_data.active))
        self.connection.commit()
        cursor.close()

    def getMatches(self, groupId='', studentId='', matchId = '', active = None, limit=10, index=0):
        cursor = self.connection.cursor()
        get_query='''SELECT matches.groupId,
                            matches.studentId,
                            matches.matchId,
                            matches.active,
                            users.firstName,
                            users.lastName
                    FROM matches
                    INNER JOIN users
                    ON matches.studentId = users.userGId
                    WHERE (matches.groupId= %s OR matches.studentId= %s OR matches.matchId =%s) OR matches.active = %s 
                    LIMIT %s OFFSET %s 
                 '''
        cursor.execute(get_query, (groupId,
                                   studentId,
                                   matchId,
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
                             active = match[3],
                             firstName = match[4],
                             lastName = match[5])
            match_list.append(m)
        cursor.close()
        return match_list
        
    def checkMatch(self, groupId, studentId):
        cursor = self.connection.cursor()
        get_query='''SELECT groupId,
                            studentId,
                            matchId,
                            active
                    FROM matches
                    WHERE groupId= %s AND studentId= %s AND active = 1
                 '''
        cursor.execute(get_query, (groupId,
                                   studentId,
                                   ))
        match = cursor.fetchall()
        if match:
            cursor.close()
            return False
        cursor.close()
        return True
            
    def updateMatch(self,active,matchId):
        cursor = self.connection.cursor()
        update_query = '''UPDATE matches
                            SET 
                                active = %s
                            WHERE matchId = %s '''
        cursor.execute(update_query, (active,matchId))
        self.connection.commit()
        cursor.close()
        
    def deleteMatch(self, matchId):
        cursor = self.connection.cursor()
        delete_query="DELETE FROM matches WHERE matchId=%s"
        cursor.execute(
            delete_query,
            (matchId,))
        self.connection.commit()
        cursor.close()



########################## MESSAGE ####################

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

################################# ATTENDANCE ##################################

    def insertAttendance(self, attendance_data, attendance = 0):
        cursor = self.connection.cursor()
        insert_query = '''INSERT INTO
                          attendances(lessonId, studentId, attendance)
                          VALUES (%s, %s, %s)'''
        cursor.execute(insert_query, (attendance_data.lessonId, attendance_data.studentId, attendance))
        self.connection.commit()
        cursor.close()

    def updateAttendance(self, attendance_data, lessonId, studentId):
        cursor = self.connection.cursor()
        update_query = '''UPDATE attendances
                            SET 
                                attendance = %s
                            WHERE (lessonId = %s AND studentId = %s) '''
        cursor.execute(update_query, (
                                    attendance_data.attendance,
                                    lessonId,
                                    studentId))
        self.connection.commit()
        cursor.close()


    def getAttendance(self, lessonId='', studentId=''):
        cursor = self.connection.cursor(buffered=True)
        get_query='''SELECT 
                        lessonId,
                        studentId, 
                        attendance,
                        attendanceId 
                    FROM attendances 
                    WHERE lessonId=%s AND studentId =%s'''
        cursor.execute(get_query, (lessonId, studentId))
        result = cursor.fetchone()
        attendance = models.Attendance(
                                        lessonId=lessonId,
                                        studentId=studentId,
                                        attendance=result[2],
                                        attendanceId=result[3])
        cursor.close()
        return attendance

################################# GRADES ##########################

    def getGrades(self,groupId = None, studentId = None, gradeId = None):
        cursor = self.connection.cursor()
        get_query='''SELECT
                        grades.gradeId,
                        grades.groupId,
                        grades.studentId,
                        grades.grade,
                        users.firstName,
                        users.lastName,
                        grades.des
                    FROM grades
                    INNER JOIN users
                    ON grades.studentId = users.userGId
                    WHERE (grades.groupId = %s AND grades.studentId = %s) OR grades.gradeId = %s'''
        cursor.execute(get_query,(groupId,studentId,gradeId))
        grades = cursor.fetchall()
        
        if not grades:
            cursor.close()
            return None

        grades_list = []
        for grade in grades:
            g = models.Grade(
                            gradeId = grade[0],
                            groupId = grade[1],
                            studentId = grade[2],
                            grade = grade[3],
                            firstName = grade[4],
                            lastName = grade[5],
                            desc = grade[6])
            grades_list.append(g)
        cursor.close()
        return grades_list

    def insertGrade(self,grade_data):
        cursor = self.connection.cursor()
        insert_query = '''INSERT INTO
                          grades(groupId, studentId, grade, des)
                          VALUES (%s, %s, %s, %s)'''
        cursor.execute(insert_query, (grade_data.groupId, grade_data.studentId, grade_data.grade, grade_data.desc))
        self.connection.commit()
        cursor.close()
