from mysql.connector import connect
from mysql.connector.errors import ProgrammingError

#Start the SQL server using the following parameters:
user = 'database'   #username (user with all permissions)
host = 'localhost'  #hostname
password = 'database'   #password
database = 'database'   #database name


create_tables_sql_guery=[]
#Add your SQL queries here (query name = table name).

users='''
    CREATE TABLE users (
    userGId varchar(50) NOT NULL,
    firstName varchar(20) NOT NULL,
    lastName varchar(20) NOT NULL,
    email varchar(40) NOT NULL,
    pass varchar(100) NOT NULL,
    user_type ENUM('student', 'teacher', 'admin'),
    active bool NOT NULL,
    PRIMARY KEY(userGId)
    );'''

subjects='''
    create table subjects(
    subjectId int NOT NULL AUTO_INCREMENT,
    name varchar(50),
    description varchar(255),
    PRIMARY KEY(subjectId)
    );'''
groups='''
    create table groups(
    groupId int NOT NULL AUTO_INCREMENT,
    active bool NOT NULL,
    subjectId int NOT NULL,
    teacherId varchar(50) NOT NULL,
    PRIMARY KEY(groupId),
    FOREIGN KEY(subjectId) REFERENCES subjects(subjectId),
    FOREIGN KEY(teacherId) REFERENCES users(userGId)
    );'''
lessons='''
    create table lessons(
    lessonId int NOT NULL AUTO_INCREMENT,
    groupId int NOT NULL,
    classroom varchar(5) NOT NULL,
    dateValue date NOT NULL,
    timeValue time NOT NULL,
    PRIMARY KEY(lessonId),
    FOREIGN KEY(groupId) REFERENCES groups(groupId)
    );'''
attendances='''
    create table attendances(
    attendanceId int NOT NULL AUTO_INCREMENT,
    lessonId int NOT NULL,
    studentId varchar(50) NOT NULL,
    attendance bool NOT NULL,
    PRIMARY KEY(attendanceId),
    FOREIGN KEY(lessonId) REFERENCES lessons(lessonId),
    FOREIGN KEY(studentId) REFERENCES users(userGId)
    );'''
grades='''
    create table grades(
    gradeId int NOT NULL AUTO_INCREMENT,
    groupId int NOT NULL,
    studentId varchar(50) NOT NULL,
    grade int NOT NULL,
    des varchar(1000) NOT NULL,
    PRIMARY KEY(gradeId),
    FOREIGN KEY(groupId) REFERENCES groups(groupId),
    FOREIGN KEY(studentId) REFERENCES users(userGId)
    );'''
matches='''
    create table matches(
    matchId int NOT NULL AUTO_INCREMENT,
    groupId int NOT NULL,
    studentId varchar(50) NOT NULL,
    active bool NOT NULL,
    PRIMARY KEY(matchId),
    FOREIGN KEY(groupId) REFERENCES groups(groupId)
    );
    '''
messages = '''
    CREATE TABLE messages(
                          messageId int NOT NULL AUTO_INCREMENT,
                          userGId varchar(50) NOT NULL,
                          author varchar(50) NOT NULL,
                          title varchar(50) NOT NULL,
                          groupId int NOT NULL,
                          message varchar(1000),
                          date datetime NOT NULL,
                          FOREIGN KEY(groupId) REFERENCES groups(groupId),
                          PRIMARY KEY(messageId)
                          )'''



def add_query_to_set(*args):
    global create_tables_sql_guery
    for arg in args:
        create_tables_sql_guery.append(arg)


def setup():
    global create_tables_sql_guery
    try:
        cnx = connect(user=user,host=host,password=password,database=database,)
        cursor = cnx.cursor()
        for query in create_tables_sql_guery:
            cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as e:
        print(e)

#Add your table name to args of this function below.
add_query_to_set(users,
                subjects,
                groups,
                lessons,
                attendances,
                grades,
                matches,
                messages,
                )

setup()
#Run this script.