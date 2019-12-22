from flask import Flask
import os
import logging

hostName = os.getenv("hostName")
port = os.getenv("port")
userName = os.getenv("userName")
password = os.getenv("password")
database = os.getenv("database")

if __name__ == '__main__':
    app = Flask(__name__)
    import urls
    from database import Database

    app.secret_key = os.urandom(24)
    app.register_blueprint(urls.apps)
    
    fh = logging.FileHandler('app.log')
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='app.log',
                    filemode='w')

    app.run(debug=True)