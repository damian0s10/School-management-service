from mysql.connector import connect, ProgrammingError


class Database(object):
    user = 'database'
    host = 'localhost'
    password = 'database'
    database = 'database'

#This method establish connection to database. 
    def connect(self):
        cnx = connect(user=Database.user,
                      host=Database.host,
                      password=Database.password,
                      database=Database.database,)
        return cnx

#This method adds user to database
    def add_user(self, user_data):
        cnx = Database.connect(self)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO users(firstName,lastName, email, pass, active) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(insert_query,
                      (user_data.first_name,
                       user_data.last_name,
                       user_data.email,
                       user_data.password,
                       1))
        cnx.commit()
        cnx.close()
#This method adds admin to administrators when name given
    def add_admin(self, ident):
        cnx = Database.connect(self)
        cursor = cnx.cursor()
        get_user_promoted_query="SELECT userId FROM users WHERE firstName = %s"
        cursor.execute(get_user_promoted_query, (ident,))
        promoted_id = cursor.fetchone()
        insert_admin_query = "INSERT INTO administrators(userId) VALUES(%s)"
        cursor.execute(insert_admin_query, (promoted_id[0],))
        cnx.commit()
        cnx.close()

#This method returns admin data when userId
    def get_admin_by_ident(self, ident):
        cnx = Database.connect(self)
        cursor = cnx.cursor()
        get_admin_query = "SELECT adminId, userId FROM administrators WHERE userId = %s"
        get_user_query = "SELECT firstName, lastName, email, pass, active FROM users WHERE userId = %s"
        cursor.execute(get_admin_query, (ident,))
        admin_data = cursor.fetchone()
        cursor.execute(get_user_query, (ident,))
        user_data = cursor.fetchone()
        admin = Administrator()
        admin.admin_id = admin_data[0]
        admin.user_id = admin_data[1]
        admin.first_name = user_data[0]
        admin.last_name = user_data[1]
        admin.email = user_data[2]
        admin.password = user_data[3]
        admin.active = user_data[4]
        cnx.close()
        return admin

#This method returns user data when name given
    def get_user_by_name(self,name):
        cnx = Database.connect(self)
        cursor = cnx.cursor()
        query = "SELECT userId, firstName, lastName, email, pass, active FROM users WHERE firstName= %s"
        cursor.execute(query, (name,) )
        results = cursor.fetchone()
        user = User()
        user.user_id = results[0]
        user.first_name = results[1]
        user.last_name = results[2]
        user.email = results[3]
        user.password = results[4]
        user.active = results[5]
        cnx.close()
        return user


        
class User(object):
    def __init__(self):
        self.user_id = None
        self.first_name = None
        self.last_name = None
        self.email = None
        self.password = None
        self.active = True
    
class Administrator(User):
    def __init__(self):
        super(Administrator,self).__init__()
        self.admin_id = None
        
   



            


