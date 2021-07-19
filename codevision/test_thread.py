from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime
import threading
import sys
import time

sys.path.append("..") #相对路径或绝对路径
from config import SQLALCHEMY_DATABASE_URI
from entity import Event

seconds=10

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
# 创建新User对象:
event_desc='有人摔倒'
event_type=0
event_date=datetime.datetime.now()
event_location='走廊'
old_people_id=107

def insert(threadName):
    while (True):
        # if lock.acquire():
        f = open('allowinsertdatabase1.txt', 'r')
        content = f.read()
        f.close()
        is_allowed = content[11:12]
        if is_allowed == '1':  # 如果允许插入
            f = open('allowinsertdatabase1.txt', 'w')
            f.write('is_allowed=0')
            f.close()
            print(threadName, '准备插入数据库')
            # 添加到session:
            event = Event(event_desc=event_desc, event_type=event_type, event_date=event_date,
                          event_location=event_location, oldperson_id=old_people_id)
            session.add(event)
            # 提交即保存到数据库:
            session.commit()
            # 关闭session:
            # session.close()
            print(threadName, '插入成功')
        else:
            pass
            # time.sleep(0.5)
def controltime(threadName):
    while True:
        f = open('allowinsertdatabase1.txt', 'r')
        content = f.read()
        f.close()

        is_allowed = content[11:12]
        # print(222, allow)
        # if lock.acquire():
        if is_allowed == '0':
            print(threadName, 'status: not allow')
            for i in range(seconds, 0, -1):
                print(threadName, 'wait %d seconds...' % (i))
                time.sleep(1)

            f = open('allowinsertdatabase1.txt', 'w')
            f.write('is_allowed=1')
            f.close()
        else:
            print(threadName, 'status: allow')
            time.sleep(1)


#多开一个线程定时控制插入
t1 = threading.Thread(target=controltime, args=("Thread1",))
t2 = threading.Thread(target=insert, args=("Thread2",))
t2.start()
t1.start()
insert('h')

session.close()

