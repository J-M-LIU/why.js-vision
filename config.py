# coding = utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# mysql配置
DIALECT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = "Stz123456"
HOST = "bj-cynosdbmysql-grp-94ctk06s.sql.tencentcdb.com"
# HOST="localhost"
PORT = "21171"
# PORT="3306"
AUTOCOMMIT=True
DATABASE = "careOld"

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE,autocommit=AUTOCOMMIT)
SQLALCHEMY_TRACK_MODIFICATIONS = False