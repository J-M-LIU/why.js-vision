# -*- coding: utf-8 -*-
'''
将事件插入数据库主程序

用法：
'''
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import time
import datetime
import argparse

import sys
sys.path.append("..") #相对路径或绝对路径
from extend import db
from entity import Event
from config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()

f = open('codevision/allowinsertdatabase4.txt', 'r')
content = f.read()
f.close()
allow = content[11:12]

if allow == '1':  # 如果允许插入

    f = open('codevision/allowinsertdatabase4.txt', 'w')
    f.write('is_allowed=0')
    f.close()
    print('准备插入数据库')

    # 传入参数
    ap = argparse.ArgumentParser()

    ap.add_argument("-ed", "--event_desc", required=False,
                    default='', help="")
    ap.add_argument("-et", "--event_type", required=False,
                    default='', help="")
    ap.add_argument("-el", "--event_location", required=False,
                    default='', help="")
    ap.add_argument("-epi", "--old_people_id", required=False,
                    default='', help="")
    args = vars(ap.parse_args())
    for arg in args:
        print (arg)

    event_desc = args['event_desc']
    event_type = int(args['event_type']) if args['event_type'] else None
    event_location = args['event_location']
    old_people_id = int(args['old_people_id']) if args['old_people_id'] else None

    event_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {'id': 0,  # id=0 means insert; id=1 means update;
               'event_desc': event_desc,
               'event_type': event_type,
               'event_date': event_date,
               'event_location': event_location,
               'oldperson_id': old_people_id}

    print('调用插入事件数据的API')
    #插入事件信息数据
    event=Event(event_desc=event_desc,event_type=event_type,event_date=event_date,
                event_location=event_location,oldperson_id=old_people_id)

    # db.session.add(event);
    # db.session.commit()

    # 添加到session:
    session.add(event)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()
    print('插入成功')
else:
    # print('pass')
    pass
