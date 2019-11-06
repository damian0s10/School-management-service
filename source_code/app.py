from flask import Flask
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
from views import *


if __name__ == '__main__':
    app.run()
