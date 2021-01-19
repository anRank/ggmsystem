import os
from datetime import timedelta

DEBUG = True

SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(days=7)


DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '000220'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'ggmsystem'

# 连接mysql数据库
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
# 'mysql+pymysql://root:000220@127.0.0.1:3306/splatform2?charset=utf8'
# print(SQLALCHEMY_DATABASE_URI)
SQLALCHEMY_TRACK_MODIFICATIONS = False
