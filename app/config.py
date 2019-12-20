import logging
import os
from database import Database

DEBUG = True
SECRET_KEY = os.urandom(24)

hostName = os.getenv("hostName")
port = os.getenv("port")
userName = os.getenv("userName")
password = os.getenv("password")
database = os.getenv("database")

fh = logging.FileHandler('app.log')
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='app.log',
                filemode='w')