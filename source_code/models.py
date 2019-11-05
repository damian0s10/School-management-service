from mysql.connector import connect, ProgrammingError


class Database(object):
    user = 'database'
    host = 'localhost'
    password = 'database'
    database = 'database'
    
    def connect(self):
        cnx = connect(user=self.user,
                      host=self.host,
                      password=self.password,
                      database=self.database,)

    def add_user(self, user_data):
        cnx = Database.connect()
        cursor = cnx.cursor()
        insert_query = "INSERT INTO users(firstName,lastName, email, pass, active) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(insert_query,
                      (user_data.first_name,
                       user_data.last_name,
                       user_data.email,
                       user_data.password,
                       0))
        cnx.commit()
        cnx.close()

    def get_user_by_name(self,name):
        cnx = Database.connect(self)
        cursor = cnx.cursor()
        query = "SELECT firstName, lastName, email, pass, active FROM users WHERE firstName= %s"
        q = "SELECT * from users"
        cursor.execute(query, (name,) )
        results = cursor.fetchone()
        user = User(results[0], results[1], results[2], results[3])
        return user
              
        
class User(object):
    def __init__(self, name, surname, email, password):
        self.first_name = name
        self.last_name = surname
        self.email = email
        self.password = password
        self.active = False
        


            


