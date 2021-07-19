# -*- coding=utf8 -*-
# 导入Flask库
import multiprocessing
import threading
from time import sleep
from keras.models import load_model
from flask import Flask
from flask import request
from flask import render_template
from flask import Response

import json
from flask import redirect, url_for
import cv2
# 导入MySQL库
import pymysql
import argparse
import config
import user
# import collectingfaces
from codevision.insertingcontrol import controltime
from variable import globalvar
from codevision.checkstrangerandfacial import checkstrangerandfacial
from codevision.checkingfalldetection import checkfall
from codevision.oldcare.camera import VideoCamera
from collectingfaces import runfacecollect
from extend import db


app = Flask(__name__)
app.config.from_object(config) #配置app.config
db.app=app
db.init_app(app)

    # API
location='yard'

global_frame=None
global_frame1=None
global_frame2=None
global_frame3=None
global_frame4=None
video_camera=None
t1=None
t2=None

print('haha')
@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera
    if video_camera == None:
        video_camera = VideoCamera()

    status = request.form.get('status')
    save_video_path = request.form.get('save_video_path')

    if status == "true":
        video_camera.start_record(save_video_path)
        return 'start record'
    else:
        video_camera.stop_record()
        return 'stop record'


#2.走廊摄像头-检测摔倒
def video_stream2():
    global video_camera
    global global_frame2
    if video_camera is None:
        #相机示例
        video_camera = VideoCamera()
        #开始检测stranger和facial
    # t2 = threading.Thread(target=checkfall,args=(video_camera,))
    # t2.start()
    while True:
        if (globalvar.get_is_begin() is True):
            frame = globalvar.get_global_frame2()
            if frame is not None:
                global_frame2 = frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + global_frame2 + b'\r\n\r\n')
    # if(globalvar.video_choice==2):


def video_stream():
    global video_camera
    global global_frame
    if video_camera is None:
        video_camera=VideoCamera()
    t1 = threading.Thread(target=checkstrangerandfacial, args=(video_camera,))
    t1.start()
    t2 = threading.Thread(target=checkfall, args=(video_camera,))
    t2.start()

#1.房间摄像头-检测陌生人和老人笑了
def video_stream1():
    global video_camera
    global global_frame1
    if video_camera is None:
        #相机示例
        video_camera = VideoCamera()
        #开始检测stranger和facial
    # t2 = threading.Thread(target=checkstrangerandfacial,args=(video_camera,))
    # t2.start()
    while True:
        if (globalvar.get_is_begin() is True):
            frame = globalvar.get_global_frame1()
            if frame is not None:
                global_frame1 = frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + global_frame1 + b'\r\n\r\n')
    # if(globalvar.video_choice==1):


@app.route('/video_viewer1')
def video_viewer1():
    return Response(video_stream1(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_viewer2')
def video_viewer2():
    return Response(video_stream2(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_choice', methods=['POST'])
def set_choice():
    choice=request.form.get('choice')
    globalvar.set_video_choice(choice)
    return render_template('cfxxx.html')

def get_Table_Data(table):
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='root',
        db='guanli', charset='utf8',
    )
    cur = conn.cursor()
    res = cur.execute("select * from " + table)
    res = cur.fetchmany(res)
    cur.close()
    conn.commit()
    conn.close()
    return res

@app.route('/', methods=['GET', 'POST'])
def home():
    global t1,t2
    global video_camera
    video_camera = VideoCamera()
    t1 = threading.Thread(target=checkstrangerandfacial, args=(video_camera,))
    # t2 = threading.Thread(target=checkfall, args=(video_camera,))
    t2 = threading.Thread(target=checkfall,args=(video_camera,))
    # t3 = threading.Thread(target=controltime, args=(10,))
    # t1=multiprocessing.Process(target=checkstrangerandfacial, args=(video_camera,))
    # t2=multiprocessing.Process(target=checkfall)
    # t3.start()
    # t1.start()
    t2.start()
    return render_template('login.html')

@app.route('/pjxq', methods=['GET'])
def pj():
    return render_template('pjxq.html')

@app.route('/collectFace',methods=['POST', 'GET'])
def cface():
    print("right")

    # return render_template('start.html')
    runfacecollect()
    return render_template('start.html')


@app.route('/collectOldInfo', methods=['POST', 'GET'])
def coi():
    return render_template('start.html')


@app.route('/pjxq2', methods=['GET'])
def pj1():
    return render_template('pjxq2.html')


@app.route('/pjxq3', methods=['GET'])
def pj2():
    return render_template('pjxq3.html')


@app.route('/pjxq4', methods=['GET'])
def pj3():
    return render_template('pjxq4.html')


# 对登录的用户名和密码进行判断
@app.route("/login", methods=['post', 'GET'])
def login():
    u = user.user()
    # data = json.loads(request.get_data())
    userName = request.form['username']
    password = request.form['password']
    result = u.login(userName, password)
    print(result[1])
    if result[1] == "登陆成功":
        return render_template('teacher_index.html')
    else:
        return render_template("login.html")


# 显示学生首页的函数，可以显示首页里的信息
@app.route('/student_index', methods=['GET'])
def student_index():
    return render_template('student_index.html')


@app.route('/teacher_index', methods=['GET'])
def teacher_index():
    return render_template('teacher_index.html')


@app.route('/jxjh', methods=['GET'])
def jxjh():
    # print posts
    return render_template('xmsb.html')


@app.route('/guanliban', methods=['GET'])
def guanliban():
    # print posts
    return render_template('oldManCollect.html')


@app.route('/paike_js', methods=['GET'])
def paike_js():
    # print posts
    return render_template('ndpf.html')


@app.route('/rec', methods=['GET'])
def rec():
    # print posts
    return render_template('recommendDoc.html')


@app.route('/doc', methods=['GET'])
def doc():
    # print posts
    return render_template('doc.html')


@app.route('/school', methods=['GET'])
def sc():
    # print posts
    return render_template('school.html')


@app.route('/xscj', methods=['GET'])
def xscj():
    # # print posts
    return render_template('oldpro.html')


@app.route('/xslb', methods=['GET'])
def xslb():
    # print posts
    return render_template('cfxxx.html')


@app.route('/tjiaoshi', methods=['GET'])
def tjiaoshi():
    # 调用数据库函数，获取数据
    data = get_Table_Data('tjiaoshi')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]
        dict_data['f'] = value[5]
        posts.append(dict_data)
    # print posts
    return render_template('student.html', posts=posts)

@app.route('/kecheng', methods=['GET'])
def kecheng():
    data = get_Table_Data('kecheng')

    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]
        dict_data['f'] = value[5]
        posts.append(dict_data)
    # print posts
    return render_template('student.html', posts=posts)


@app.route('/zhuanye', methods=['GET'])
def zhuanye():
    # 调用数据库函数，获取数据
    data = get_Table_Data('zhuanye')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]
        posts.append(dict_data)
    # print posts
    return render_template('student.html', posts=posts)


@app.route('/xueyuan', methods=['GET'])
def xueyuan():
    # 调用数据库函数，获取数据
    data = get_Table_Data('xueyuan')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        posts.append(dict_data)
    # print posts
    return render_template('student.html', posts=posts)


@app.route('/js', methods=['GET'])
def js():
    # 调用数据库函数，获取数据
    data = get_Table_Data('jiaoshi')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]
        dict_data['f'] = value[5]
        dict_data['g'] = value[6]
        dict_data['h'] = value[7]
        dict_data['i'] = value[8]
        dict_data['j'] = value[9]
        posts.append(dict_data)
    # print posts
    return render_template('xscj.html', posts=posts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5001)