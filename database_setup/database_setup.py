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
    userId int NOT NULL AUTO_INCREMENT,
    firstName varchar(20) NOT NULL,
    lastName varchar(20) NOT NULL,
    email varchar(40) NOT NULL,
    pass varchar(100) NOT NULL,
    active bool NOT NULL,
    PRIMARY KEY(userID)
    );'''
administrators='''
    create table administrators (
    adminId int NOT NULL AUTO_INCREMENT,
    userId int NOT NULL,
    PRIMARY KEY(adminId),
    FOREIGN KEY(userId) REFERENCES users(userId)
    );'''
teachers='''
    create table teachers (
    teacherId int NOT NULL AUTO_INCREMENT,
    userId int NOT NULL,
    PRIMARY KEY(teacherId),
    FOREIGN KEY(userId) REFERENCES users(userId)
    );'''
students='''
    create table students (
    studentId int NOT NULL AUTO_INCREMENT,
    userId int NOT NULL,
    PRIMARY KEY(studentId),
    FOREIGN KEY(userId) REFERENCES users(userId)
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
    PRIMARY KEY(groupId)
    );'''
lessons='''
    create table lessons(
    lessonId int NOT NULL AUTO_INCREMENT,
    subjectId int NOT NULL,
    teacherId int NOT NULL,
    groupId int NOT NULL,
    classroom varchar(5) NOT NULL,
    datevValue date NOT NULL,
    timeValue time NOT NULL,
    PRIMARY KEY(lessonId),
    FOREIGN KEY(subjectId) REFERENCES subjects(subjectId),
    FOREIGN KEY(teacherId) REFERENCES teachers(teacherId),
    FOREIGN KEY(groupId) REFERENCES groups(groupId)
    );'''
attendances='''
    create table attendances(
    attendanceId int NOT NULL AUTO_INCREMENT,
    lessonId int NOT NULL,
    studentId int NOT NULL,
    attendance bool NOT NULL,
    PRIMARY KEY(attendanceId),
    FOREIGN KEY(lessonId) REFERENCES lessons(lessonId),
    FOREIGN KEY(studentId) REFERENCES students(studentId)
    );'''
grades='''
    create table grades(
    gradeId int NOT NULL AUTO_INCREMENT,
    subjectId int NOT NULL,
    studentId int NOT NULL,
    grade int NOT NULL,
    PRIMARY KEY(gradeId),
    FOREIGN KEY(subjectId) REFERENCES subjects(subjectId),
    FOREIGN KEY(studentId) REFERENCES students(studentId)
    );'''
matches='''
    create table matches(
    matchId int NOT NULL AUTO_INCREMENT,
    groupId int NOT NULL,
    studentId int NOT NULL,
    PRIMARY KEY(matchId),
    FOREIGN KEY(groupId) REFERENCES groups(groupId)
    );
    '''


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
                administrators,
                teachers,
                students,
                subjects,
                groups,
                lessons,
                attendances,
                grades,
                matches)

setup()
#Run this script.