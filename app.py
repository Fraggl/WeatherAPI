rom flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

from routes import *;

if __name__ == '__main__':
    app.run(host='192.168.178.46')
