from flask import Flask
import os
from database import Database
from views import LoginView, RegisterView, IndexView, UserView, Logout

app = Flask(__name__)
app.secret_key = os.urandom(24)


if __name__ == '__main__':
    db = Database("localhost", 3306, "database", "database", "database")

    indexView = IndexView.as_view('index_view')
    app.add_url_rule('/', view_func=indexView, methods=['GET',])

    loginView = LoginView.as_view('login_view', database=db)
    app.add_url_rule('/login/', view_func=loginView,methods=['GET',])
    app.add_url_rule('/login/', view_func=loginView, methods=['POST',])

    registerView = RegisterView.as_view('register_view', database=db)
    app.add_url_rule('/register/', view_func=registerView, methods=['GET',])
    app.add_url_rule('/register/', view_func=registerView, methods=['POST',])
    
    userView = UserView.as_view('user_view', database = db)
    app.add_url_rule('/userview/', view_func=userView, methods=['GET',])

    logoutView = Logout.as_view("logout_view")
    app.add_url_rule('/logout/', view_func=logoutView, methods=['GET',])
    app.run(debug=True)