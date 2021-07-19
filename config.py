# coding = utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# mysql配置
DIALECT = "mysql"
DRIVER = "pymysql"
USERNAME = ""
PASSWORD = ""
HOST = ""
# HOST="localhost"
PORT = ""
# PORT="3306"
AUTOCOMMIT=True
DATABASE = "careOld"

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE,autocommit=AUTOCOMMIT)
SQLALCHEMY_TRACK_MODIFICATIONS = False