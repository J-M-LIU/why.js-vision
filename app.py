# -*- coding=utf8 -*-
# 导入Flask库

from flask import Flask, session, g, flash
import json
from flask import redirect, url_for
import cv2
# 导入MySQL库
import pymysql

import employee
import old

# import collectingfaces
# from collectingfaces import runfacecollect
import volunteer
from collectingfaces1 import runfacecollect

app = Flask(__name__)

# use 0 for web camera

import threading
from flask import request
from flask import render_template
from flask import Response

import json
import cv2
# 导入MySQL库
import pymysql
import user
from codevision.insertingcontrol import controltime
from variable import globalvar
from codevision.checkstrangerandfacial import checkstrangerandfacial
from codevision.checkingfalldetection import checkfall
from codevision.checkingfence import checkfence
from codevision.checkingvolunteeractivity import checkactivity
from codevision.oldcare.camera import VideoCamera
from codevision.trainingfacerecognition import trainfacerecognition
# from collectingfaces import runfacecollect
from extend import db

flag = ""
idd= ""
result = []
totalId=""
oldId = ""
EmployId = ""
VolunId = ""
    # API
location='yard'

global_frame=None
global_frame1=None
global_frame2=None
global_frame3=None
global_frame4=None
video_camera=None
video_camera1=None
video_camera2=None
video_camera3=None
video_camera4=None
video_camera5=None

t1=None
t2=None
t3=None
t4=None

gc=None

timeF=24

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
    global video_camera2
    global global_frame2
    global gc
    if video_camera2 is None:
        #相机示例
        video_camera2 = VideoCamera()
        #开始检测stranger和facial
    while True:
        if (globalvar.get_is_begin() is True and gc=='走廊摄像头'):
            frame = globalvar.get_global_frame2()
            if frame is not None:
                global_frame2 = frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + global_frame2 + b'\r\n\r\n')
        else:
            break

#1.房间摄像头-检测陌生人和老人笑了
def video_stream1():
    global video_camera1
    global global_frame1
    global timeF
    if video_camera1 is None:
        #相机示例
        video_camera1 = VideoCamera()
    while True:
        # frame=video_camera1.get_frame()
        # if frame is not None:
        #     global_frame1 = frame
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # else:
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + global_frame1 + b'\r\n\r\n')
        if (globalvar.get_is_begin() is True and gc=='房间摄像头'):
            frame = globalvar.get_global_frame1()
            if frame is not None:
                global_frame1 = frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + global_frame1 + b'\r\n\r\n')

        else:
            break

#3.院子摄像头-禁止区域入侵检测
def video_stream3():
    global video_camera3
    global global_frame3
    global timeF,gc
    if video_camera3 is None:
        #相机示例
        video_camera3 = VideoCamera()
    while True:
        # frame=video_camera1.get_frame()
        # if frame is not None:
        #     global_frame1 = frame
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # else:
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + global_frame1 + b'\r\n\r\n')
        if (globalvar.get_is_begin() is True and gc=='院子摄像头'):
            frame = globalvar.get_global_frame3()
            if frame is not None:
                global_frame3 = frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + global_frame3 + b'\r\n\r\n')
        else:
            break

#4.桌子摄像头-义工交互检测
def video_stream4():
    global video_camera4
    global global_frame4
    global timeF,gc
    if video_camera4 is None:
        #相机示例
        video_camera4 = VideoCamera()
    while True:
        # frame=video_camera1.get_frame()
        # if frame is not None:
        #     global_frame1 = frame
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # else:
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + global_frame1 + b'\r\n\r\n')
        if (globalvar.get_is_begin() is True and gc=='桌子摄像头'):
            frame = globalvar.get_global_frame4()
            if frame is not None:
                global_frame4 = frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + global_frame4 + b'\r\n\r\n')
        else:
            break


@app.route('/video_viewer1')
def video_viewer1():
    return Response(video_stream1(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_viewer2')
def video_viewer2():
    return Response(video_stream2(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_viewer3')
def video_viewer3():
    return Response(video_stream3(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_viewer4')
def video_viewer4():
    return Response(video_stream4(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_viewer5')
def video_viewer5():
    return Response(video_stream5(), mimetype='multipart/x-mixed-replace; boundary=frame')
flagg=""
def video_stream5():
    global video_camera5
    global global_frame5
    global idd,totalId
    globalvar.set_collect(True)
    t5 = threading.Thread(target=runfacecollect, args=(idd, str(totalId),))
    t5.start()
    while True:
        while True:
            if (globalvar.get_is_begin() is True):
                if (globalvar.get_collect() is False):
                    break
                else:
                    frame = globalvar.get_global_frame5()
                    if frame is not None:
                        global_frame5 = frame
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                    else:
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + global_frame5 + b'\r\n\r\n')
        global flagg
        flagg="采集完毕"


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

# 跳转摄像机
@app.route("/chooseCamera", methods=['GET', 'post'])
def gbb():
    global gc
    gc = request.form['gc']
    # if gc == "电脑摄像头":
    #     return render_template('cfxx.html',gc=gc)
    if gc == "房间摄像头":
        return render_template('cfxx1.html', gc=gc)
    if gc == "走廊摄像头":
        return render_template('cfxx2.html', gc=gc)
    if gc == "院子摄像头":
        return render_template('cfxx3.html', gc=gc)
    if gc == "桌子摄像头":
        return render_template('cfxx4.html', gc=gc)

    # return render_template('start.html')
    # runfacecollect()
    return render_template('cfxx.html',gc=gc)

@app.route('/', methods=['GET', 'POST'])
def home():
    global t1, t2,t3,t4
    global video_camera1,video_camera2,video_camera3,video_camera4
    # video_camera1 = VideoCamera()
    # video_camera2 = VideoCamera()
    # video_camera3 = VideoCamera()
    # video_camera4 = VideoCamera()
    # video_camera2 = VideoCamera('rtsp://192.168.137.99/test2')
    # video_camera4 = VideoCamera('rtsp://192.168.137.10/test2')
    # video_camera4=VideoCamera('rtsp://192.168.137.99/test2')
    t1 = threading.Thread(target=checkstrangerandfacial, args=(video_camera1,))
    t2 = threading.Thread(target=checkfall, args=(video_camera2,))
    t3=threading.Thread(target=checkfence,args=(video_camera3,))
    t4=threading.Thread(target=checkactivity,args=(video_camera4,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    # t5 = threading.Thread(target=controltime, args=(10,))
    # t5.start()
    return render_template('login.html')
    return render_template('login.html')

@app.route('/pjxq', methods=['GET'])
def pj():
    return render_template('pjxq.html')

@app.route('/guanliban', methods=['GET', 'POST'])
def guanliban():
    # print posts
    u = old.old()
    result = u.queryAll()
    print(result)
    qq = [[0 for i in range(30)] for i in range(result[2][0][0])]
    # qq = [[[] for i in range(30)] for i in range(4)]
    i = 0

    #
    # # img_path = 'D://Download/mima.jpg'
    # # img_stream = return_img_stream(img_path)
    for i in range(result[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/old_people/' + str(result[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        print(i)
        qq[i][0] = result[3][i][0]
        qq[i][3] = result[3][i][3]
        qq[i][4] = result[3][i][4]
        qq[i][29] = result[3][i][29]
        qq[i][5] = result[3][i][5]
        qq[i][6] = result[3][i][6]
        qq[i][7] = result[3][i][7]
        qq[i][13] = result[3][i][13]
        qq[i][14] = result[3][i][14]
        qq[i][15] = result[3][i][15]


    return render_template('oldManCollect.html', u=qq)

def cface():
    global flag
    flag = "已完成采集"
    print(flag)
    # return render_template('start.html')
    # runfacecollect()
    return render_template('start.html', flag="已完成采集")


@app.route('/collectOldInfo', methods=['POST', 'GET'])
def coi():
    return render_template('start.html')


@app.route('/collectEmployeeInfo', methods=['POST', 'GET'])
def cei():
    return render_template('start1.html')


@app.route('/collectVolunInfo', methods=['POST', 'GET'])
def ceii():
    return render_template('start2.html')


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
    global result
    result = u.login(userName, password)
    print(result)
    # print(g.id)
    if result[1] == "登陆成功":
        return render_template('teacher_index.html')
    else:
        return render_template("login.html")


@app.route("/goregister", methods=['post', 'GET'])
def goregister():
    return render_template("register.html")


@app.route("/register", methods=['post', 'GET'])
def register():
    # return render_template("register.html")
    # @app.route("/register", methods=['post', 'GET'])
    # def register():
    print("right")
    u = user.user()
    username = request.form['username1']
    password = request.form['password1']
    real_name = request.form['realname']
    sex = 'null'
    email = request.form['email']
    phone = request.form['phone']
    result = u.register(username, password, real_name, sex, email, phone)
    print(result)
    return render_template("login.html")


# 显示学生首页的函数，可以显示首页里的信息
@app.route('/student_index', methods=['GET'])
def student_index():
    return render_template('student_index.html')


@app.route('/teacher_index', methods=['GET'])
def teacher_index():
    return render_template('teacher_index.html')


# @app.route('/jxjh', methods=['GET'])
# def jxjh():
#     # print posts
#     return render_template('volunCollect.html', u=queryEmployee())


@app.route('/jxjh', methods=['GET'])
def jxjh():
    # print posts
    # img_path = '/home/reed/caresystem/images/faces/employees/88/smile_10.jpg'
    # img_stream = return_img_stream(img_path)

    print(queryEmployee()[2][0][0])
    qq = [[0 for i in range(20)] for i in range(queryEmployee()[2][0][0])]

    # img_path = 'D://Download/mima.jpg'
    # img_stream = return_img_stream(img_path)
    for i in range(queryEmployee()[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/employees/' + str(queryEmployee()[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        qq[i][0] = queryEmployee()[3][i][0]
        qq[i][3] = queryEmployee()[3][i][3]
        qq[i][4] = queryEmployee()[3][i][4]
        qq[i][19] = queryEmployee()[3][i][19]
        qq[i][7] = queryEmployee()[3][i][7]
        qq[i][6] = queryEmployee()[3][i][6]
    #
    # print(qq[1])
    return render_template('volunCollect.html', u=qq)

def queryEmployee():
    u = employee.employee()
    result = u.queryAll()
    print(result)
    return result

def return_img_stream(img_local_path):
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream



# @app.route("/volunteer/query", methods=['post'])
def queryVolunteer():
    u = volunteer.volunteer()
    result = u.queryAll()
    return result


def queryEmployee():
    u = employee.employee()
    result = u.queryAll()
    print(result)
    return result


@app.route('/paike_js', methods=['GET'])
def paike_js():
    # print posts

    print(queryVolunteer())
    qq = [[0 for i in range(20)] for i in range(queryVolunteer()[2][0][0])]
    #
    # # img_path = 'D://Download/mima.jpg'
    # # img_stream = return_img_stream(img_path)
    for i in range(queryVolunteer()[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/volunteers/' + str(queryVolunteer()[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        qq[i][0] = queryVolunteer()[3][i][0]
        qq[i][3] = queryVolunteer()[3][i][3]
        qq[i][4] = queryVolunteer()[3][i][4]
        qq[i][19] = queryVolunteer()[3][i][19]
        qq[i][7] = queryVolunteer()[3][i][7]
        qq[i][6] = queryVolunteer()[3][i][6]

    return render_template('realVoluCollect.html', u=qq)


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


def getold():
    user = old.old()
    res = user.ageStatistics()[2]
    return res


def getEmp():
    user = employee.employee()
    res = user.ageStatistics()[2]
    return res


def getVol():
    user = volunteer.volunteer()
    res = user.ageStatistics()[2]
    return res


def getEvent():
    user1 = user.user()
    return user1.eventStatistics1()

@app.route('/xscj', methods=['GET', 'post'])
def xscj():
    # # print posts
    print(getEvent()[8])
    info1 = []
    rr = request.form.get('sd')
    print(rr)
    if rr == "全部":
        info1 = getEvent()[8]
    if rr == "笑容情况":
        info1 = getEvent()[3]
    if rr == "陌生人情况":
        info1 = getEvent()[5]
    if rr == "义工与老人交护":
        info1 = getEvent()[4]
    if rr == "摔倒统计":
        info1 = getEvent()[6]
    if rr == "禁区入侵":
        info1 = getEvent()[7]

    return render_template('showCData.html', olddata=getold(), employdata=getEmp(), volundata=getVol(), info=info1,
                           rr=rr)

@app.route('/xslb', methods=['GET'])
def xslb():
    # print posts
    return render_template('cfxx.html')


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



@app.route("/addOldInfo", methods=['post', 'GET'])
def addOldInfo():
    u = old.old()
    # data = json.loads(request.get_data())
    username = request.form['xingming']
    gender = request.form['sex']
    age = request.form['age']
    phone = request.form['phone']
    id_card = request.form['credit_id']
    global result
    CREATEBY = result[2][0]
    birthday = request.form['birthday']
    firstguardian_name = request.form['firstguardian_name']
    firstguardian_relationship = request.form['firstguardian_relationship']
    firstguardian_phone = request.form['firstguardian_phone']
    result1 = u.addInfo(username, gender, age, phone, id_card, birthday, CREATEBY, firstguardian_name
                        , firstguardian_relationship, firstguardian_phone)

    print(result1)
    global oldId,totalId,idd
    oldId = result1[0]
    totalId=oldId
    idd=0

    global flag
    flag = "已完成采集"
    print(flag)
    # return render_template('start.html')
    # runfacecollect()
    return render_template('room2.html', flag="已完成采集", username=request.form['xingming'],
                           gender=request.form['sex'],
                           age=request.form['age'],
                           phone=request.form['phone'],
                           id_card=request.form['credit_id'],
                           CREATEBY=result[2][0],
                           birthday=request.form['birthday'],
                           firstguardian_name=request.form['firstguardian_name'],
                           firstguardian_relationship=request.form['firstguardian_relationship'],
                           firstguardian_phone=request.form['firstguardian_phone'],
                           )


# @app.route("/old/addInfo", methods=['post'])
# def addOldInfo():
#     u = old.old()
#     data = json.loads(request.get_data())
#     username =request.form['xingming']
#     gender = request.form['sex']
#     age = data['age']
#     phone = data['phone']
#     id_card = data['id_card']
#     birthday = data['birthday']
#     CREATEBY = data['CREATEBY']
#     firstguardian_name = data['firstguardian_name']
#     firstguardian_relationship = data['firstguardian_relationship']
#     firstguardian_phone = data['firstguardian_phone']
#     result = u.addInfo(username, gender, age, phone, id_card, birthday, CREATEBY, firstguardian_name
#                        , firstguardian_relationship, firstguardian_phone)
#     return result

@app.route("/addOldImage", methods=['post', 'GET'])
def addOldImage():
    u = old.old()
    global oldId
    # data = json.loads(request.get_data())
    id = oldId
    imgset_dir = "/home/reed/caresystem/images/faces/old_people" + str(id)
    result = u.addImage(id, imgset_dir)
    print(result)
    return render_template('teacher_index.html')


@app.route("/addVolunImage", methods=['post', 'GET'])
def addVolunImage():
    u = volunteer.volunteer()
    global VolunId
    id = VolunId
    imgset_dir = "/home/reed/caresystem/images/faces/volunteers" + str(id)

    result = u.addImage(id, imgset_dir)
    return render_template('teacher_index.html')


@app.route("/addEmployeeImage", methods=['post', 'GET'])
def addEmployeeImage():
    u = employee.employee()
    global EmployId
    id = EmployId
    imgset_dir = "/home/reed/caresystem/images/faces/employees" + str(id)
    result = u.addImage(id, imgset_dir)
    return render_template('teacher_index.html')


# 获取老人数据
def queryOld():
    u = old.old()
    result = u.queryAll()
    print(result)
    return result


# 老人模糊查询
@app.route("/queryoldFuzzy", methods=['GET', 'post'])
def oldFuzzy():
    u = old.old()
    # data = json.loads(request.get_data())
    query = request.form['searchOld']
    result = u.queryFuzzy(query)
    print(result)
    qq = [[0 for i in range(30)] for i in range(result[2][0][0])]
    # qq = [[[] for i in range(30)] for i in range(4)]
    i = 0

    #
    # # img_path = 'D://Download/mima.jpg'
    # # img_stream = return_img_stream(img_path)
    for i in range(result[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/old_people/' + str(result[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        print(i)
        qq[i][0] = result[3][i][0]
        qq[i][3] = result[3][i][3]
        qq[i][4] = result[3][i][4]
        qq[i][29] = result[3][i][29]
        qq[i][5] = result[3][i][5]
        qq[i][6] = result[3][i][6]
        qq[i][7] = result[3][i][7]
        qq[i][13] = result[3][i][13]
        qq[i][14] = result[3][i][14]
        qq[i][15] = result[3][i][15]

    return render_template('oldManCollect.html', u=qq)


# 员工模糊查询
@app.route("/queryEmployFuzzy", methods=['GET', 'post'])
def employFuzzy():
    u = employee.employee()
    # data = json.loads(request.get_data())
    query = request.form['searchEmploy']

    print(query)
    result = u.queryFuzzy(query)
    print(result)
    qq = [[0 for i in range(20)] for i in range(result[2][0][0])]

    # img_path = 'D://Download/mima.jpg'
    # img_stream = return_img_stream(img_path)
    for i in range(result[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/employees/' + str(result[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        qq[i][0] = result[3][i][0]
        qq[i][3] = result[3][i][3]
        qq[i][4] = result[3][i][4]
        qq[i][19] = result[3][i][19]
        qq[i][7] = result[3][i][7]
        qq[i][6] = result[3][i][6]
    #
    # print(qq[1])
    return render_template('volunCollect.html', u=qq)




# 义工模糊查询
@app.route("/queryVolunFuzzy", methods=['GET', 'post'])
def volunFuzzy():
    u = volunteer.volunteer()
    # data = json.loads(request.get_data())
    query = request.form['searchVolun']

    print(query)
    result = u.queryFuzzy(query)
    print(result)
    qq = [[0 for i in range(20)] for i in range(result[2][0][0])]
    #
    # # img_path = 'D://Download/mima.jpg'
    # # img_stream = return_img_stream(img_path)
    for i in range(result[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/volunteers/' + str(result[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        qq[i][0] = result[3][i][0]
        qq[i][3] = result[3][i][3]
        qq[i][4] = result[3][i][4]
        qq[i][19] = result[3][i][19]
        qq[i][7] = result[3][i][7]
        qq[i][6] = result[3][i][6]

    return render_template('realVoluCollect.html', u=qq)


# 老人修改信息
@app.route("/gomodifyOldInfo/<oid>/<username>/<sex>/<age>/<phone>/<credit_id>/<birthday>/<firstguardian_name>/<firstguardian_relationship>/<firstguardian_phone>",
    methods=['GET', 'post'])
def gomodifyOld(oid, username, sex, age, phone, credit_id, birthday, firstguardian_name, firstguardian_relationship,
                firstguardian_phone):
    # data = json.loads(request.get_data())
    ID = oid
    username = username
    gender = sex
    age = age
    phone = phone
    id_card = credit_id
    global result
    UPDATEBY = result[2][0]
    birthday = birthday
    firstguardian_name = firstguardian_name
    print(firstguardian_name)
    firstguardian_relationship = firstguardian_relationship
    firstguardian_phone = firstguardian_phone
    return render_template('modifyOld.html', username=username, ID=oid,
                           gender=sex,
                           age=age,
                           phone=phone,
                           id_card=credit_id,
                           CREATEBY=result[2][0],
                           birthday=birthday,
                           firstguardian_name=firstguardian_name.replace(' ', ''),
                           firstguardian_relationship=firstguardian_relationship,
                           firstguardian_phone=firstguardian_phone,
                           )

# 前往修改员工信息
@app.route("/gomodifyEmployInfo/<eid>/<username>/<sex>/<age>/<phone>/<birthday>/<credit_id>", methods=['GET', 'post'])
def gomodifyEmploy(eid, username, sex, age, phone, birthday, credit_id):
    ID = eid
    username = username
    gender = sex
    age = age
    phone = phone
    id_card = credit_id
    global result
    UPDATEBY = result[2][0]
    birthday = birthday
    print(birthday)
    return render_template('modifyEmploy.html', username=username, ID=eid,
                           gender=sex,
                           age=age,
                           phone=phone,
                           id_card=credit_id.replace(' ', ''),
                           UPDATEBY=result[2][0],
                           birthday=birthday,
                           )

# 前往修改义工信息
@app.route("/gomodifyRVolunInfo/<sid>/<username>/<sex>/<age>/<phone>/<birthday>/<credit_id>", methods=['GET', 'post'])
def gomodifyRVolun(sid, username, sex, age, phone, birthday, credit_id):
    ID = sid
    username = username
    gender = sex
    age = age
    phone = phone
    id_card = credit_id
    global result
    UPDATEBY = result[2][0]
    birthday = birthday
    print(birthday)
    return render_template('modifyVolun.html', username=username, ID=sid,
                           gender=sex,
                           age=age,
                           phone=phone,
                           id_card=credit_id.replace(' ', ''),
                           UPDATEBY=result[2][0],
                           birthday=birthday,
                           )

# 前往修改员工信息
@app.route("/gomodifyVolunInfo/<vid>/<username>/<sex>/<age>/<phone>/<birthday>/<credit_id>", methods=['GET', 'post'])
def gomodifyVolun(vid, username, sex, age, phone, birthday, credit_id):
    ID = vid
    username = username
    gender = sex
    age = age
    phone = phone
    id_card = credit_id
    global result
    UPDATEBY = result[2][0]
    birthday = birthday
    print(birthday)
    return render_template('modifyEmploy.html', username=username, ID=vid,
                           gender=sex,
                           age=age,
                           phone=phone,
                           id_card=credit_id.replace(' ', ''),
                           UPDATEBY=result[2][0],
                           birthday=birthday,
                           )

# 修改义工信息
@app.route("/modifyVolunInfo/<sid>", methods=['GET', 'post'])
def modifyVolun(sid):
    # data = json.loads(request.get_data())
    u = volunteer.volunteer()
    ID = sid
    username = request.form['xingming']
    gender = request.form['sex']
    age = request.form['age']
    phone = request.form['phone']
    id_card = request.form['credit_id']
    global result
    UPDATEBY = result[2][0]
    birthday = request.form['birthday']
    result1 = u.modifyVolunteer(ID, username, gender, age, phone, id_card, birthday, UPDATEBY)
    qq = [[0 for i in range(20)] for i in range(queryVolunteer()[2][0][0])]
    #
    # # img_path = 'D://Download/mima.jpg'
    # # img_stream = return_img_stream(img_path)
    for i in range(queryVolunteer()[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/volunteers/' + str(queryVolunteer()[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        qq[i][3] = queryVolunteer()[3][i][3]
        qq[i][4] = queryVolunteer()[3][i][4]
        qq[i][19] = queryVolunteer()[3][i][19]
        qq[i][7] = queryVolunteer()[3][i][7]
        qq[i][6] = queryVolunteer()[3][i][6]

    return render_template('realVoluCollect.html', u=qq)


# 修改员工信息
@app.route("/modifyEmployInfo/<eid>", methods=['GET', 'post'])
def modifyEmploy(eid):
    # data = json.loads(request.get_data())
    u = employee.employee()
    ID = eid
    username = request.form['xingming']
    gender = request.form['sex']
    age = request.form['age']
    phone = request.form['phone']
    id_card = request.form['credit_id']
    global result
    UPDATEBY = result[2][0]
    birthday = request.form['birthday']
    result1 = u.modifyEmployee(ID, username, gender, age, phone, id_card, birthday, UPDATEBY)
    print(result1)
    qq = [[0 for i in range(20)] for i in range(queryEmployee()[2][0][0])]

    # img_path = 'D://Download/mima.jpg'
    # img_stream = return_img_stream(img_path)
    for i in range(queryEmployee()[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/employees/' + str(queryEmployee()[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        qq[i][3] = queryEmployee()[3][i][3]
        qq[i][4] = queryEmployee()[3][i][4]
        qq[i][19] = queryEmployee()[3][i][19]
        qq[i][7] = queryEmployee()[3][i][7]
        qq[i][6] = queryEmployee()[3][i][6]
    #
    # print(qq[1])
    return render_template('volunCollect.html', u=qq)
@app.route("/modifyoldInfo/<id>", methods=['GET', 'post'])
def modifyOld(id):
    u = old.old()
    # data = json.loads(request.get_data())
    ID = id
    username = request.form['xingming']
    gender = request.form['sex']
    age = request.form['age']
    phone = request.form['phone']
    id_card = request.form['credit_id']
    global result
    UPDATEBY = result[2][0]
    birthday = request.form['birthday'],
    firstguardian_name = request.form['firstguardian_name'],
    firstguardian_relationship = request.form['firstguardian_relationship'],
    firstguardian_phone = request.form['firstguardian_phone'],
    result = u.modifyOld(ID, username, gender, age, phone, id_card, birthday, UPDATEBY, firstguardian_name
                         , firstguardian_relationship, firstguardian_phone)
    result = u.queryAll()
    print(result)
    qq = [[0 for i in range(30)] for i in range(result[2][0][0])]
    # qq = [[[] for i in range(30)] for i in range(4)]
    i = 0

    #
    # # img_path = 'D://Download/mima.jpg'
    # # img_stream = return_img_stream(img_path)
    for i in range(result[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/old_people/' + str(result[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        print(i)
        qq[i][0] = result[3][i][0]
        qq[i][3] = result[3][i][3]
        qq[i][4] = result[3][i][4]
        qq[i][29] = result[3][i][29]
        qq[i][5] = result[3][i][5]
        qq[i][6] = result[3][i][6]
        qq[i][7] = result[3][i][7]
        qq[i][13] = result[3][i][13]
        qq[i][14] = result[3][i][14]
        qq[i][15] = result[3][i][15]

    return render_template('oldManCollect.html', u=qq)

# 删除老人
@app.route("/deleteold/<id>", methods=['GET', 'post'])
def deleteOld(id):
    u = old.old()
    print(id)
    # data = json.loads(request.get_data())
    ID = id
    result = u.deleteOld(ID)
    print(result)
    result = u.queryAll()
    print(result)
    qq = [[0 for i in range(30)] for i in range(result[2][0][0])]
    # qq = [[[] for i in range(30)] for i in range(4)]
    i = 0

    #
    # # img_path = 'D://Download/mima.jpg'
    # # img_stream = return_img_stream(img_path)
    for i in range(result[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/old_people/' + str(result[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        print(i)
        qq[i][0] = result[3][i][0]
        qq[i][3] = result[3][i][3]
        qq[i][4] = result[3][i][4]
        qq[i][29] = result[3][i][29]
        qq[i][5] = result[3][i][5]
        qq[i][6] = result[3][i][6]
        qq[i][7] = result[3][i][7]
        qq[i][13] = result[3][i][13]
        qq[i][14] = result[3][i][14]
        qq[i][15] = result[3][i][15]

    return render_template('oldManCollect.html', u=qq)
# 删除义工
@app.route("/deletevolun/<id>", methods=['post', 'GET'])
def deleteVolunteer(id):
    u = volunteer.volunteer()
    ID = id
    result = u.deleteVolunteer(ID)
    qq = [[0 for i in range(20)] for i in range(queryVolunteer()[2][0][0])]
    #
    # # img_path = 'D://Download/mima.jpg'
    # # img_stream = return_img_stream(img_path)
    for i in range(queryVolunteer()[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/volunteers/' + str(queryVolunteer()[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        qq[i][3] = queryVolunteer()[3][i][3]
        qq[i][4] = queryVolunteer()[3][i][4]
        qq[i][19] = queryVolunteer()[3][i][19]
        qq[i][7] = queryVolunteer()[3][i][7]
        qq[i][6] = queryVolunteer()[3][i][6]

    return render_template('realVoluCollect.html', u=qq)


# 删除员工
@app.route("/deleteemploy/<id>", methods=['GET', 'post'])
def deleteemploy(id):
    u = employee.employee()
    print(id)
    # data = json.loads(request.get_data())
    ID = id
    result = u.deleteEmployee(ID)
    print(result)
    qq = [[0 for i in range(20)] for i in range(queryEmployee()[2][0][0])]

    # img_path = 'D://Download/mima.jpg'
    # img_stream = return_img_stream(img_path)
    for i in range(queryEmployee()[2][0][0]):
        #
        img_path = '/home/reed/caresystem/images/faces/employees/' + str(queryEmployee()[3][i][0]) + "/smile_10.jpg"
        qq[i][1] = return_img_stream(img_path)
        # mylist.append(return_img_stream(img_path))
        qq[i][3] = queryEmployee()[3][i][3]
        qq[i][4] = queryEmployee()[3][i][4]
        qq[i][19] = queryEmployee()[3][i][19]
        qq[i][7] = queryEmployee()[3][i][7]
        qq[i][6] = queryEmployee()[3][i][6]
    #
    # print(qq[1])
    return render_template('volunCollect.html', u=qq)

# 添加义工信息
@app.route("/addvolunInfo", methods=['GET', 'post'])
def addVolunInfo():
    u = volunteer.volunteer()
    name = request.form['xingming']
    gender = request.form['sex']
    age = request.form['age']
    phone = request.form['phone']
    id_card = request.form['credit_id']
    birthday = request.form['birthday']
    global result
    CREATEBY = result[2][0]
    result1 = u.addInfo(name, gender, age, phone, id_card, birthday, CREATEBY)
    print(result1)
    global VolunId,idd,totalId
    VolunId = result1[2]
    totalId=VolunId
    idd=1
    global flag
    flag = "已完成采集"
    print(flag)
    # return render_template('start.html')

    # t = threading.Thread(target=trainfacerecognition)
    # t.start()
    # runfacecollect()
    return render_template('room.html', flag="已完成采集", username=request.form['xingming'],
                           gender=request.form['sex'],
                           age=request.form['age'],
                           phone=request.form['phone'],
                           id_card=request.form['credit_id'],
                           CREATEBY=result[2][0],
                           birthday=request.form['birthday'],
                           )


# 添加员工信息
@app.route("/addemployeeInfo", methods=['GET', 'post'])
def addEmployeeInfo():
    u = employee.employee()
    name = request.form['xingming']
    gender = request.form['sex']
    age = request.form['age']
    phone = request.form['phone']
    id_card = request.form['credit_id']
    birthday = request.form['birthday']
    global result
    CREATEBY = result[2][0]
    result1 = u.addInfo(name, gender, age, phone, id_card, birthday, CREATEBY)
    print(result1)
    global EmployId,idd,totalId
    EmployId = result1[2]
    totalId=EmployId
    idd=2
    # runfacecollect(2,str(EmployId))

    global flag
    flag = "已完成采集"
    print(flag)
    # t = threading.Thread(target=trainfacerecognition)
    # t.start()
    # return render_template('start1.html', flag="已完成采集", username=request.form['xingming'],
    #                        gender=request.form['sex'],
    #                        age=request.form['age'],
    #                        phone=request.form['phone'],
    #                        id_card=request.form['credit_id'],
    #                        CREATEBY=result[2][0],
    #                        birthday=request.form['birthday'],
    #                        )

    return render_template('room3.html', flag="开始采集", username=request.form['xingming'],
                           gender=request.form['sex'],
                           age=request.form['age'],
                           phone=request.form['phone'],
                           id_card=request.form['credit_id'],
                           CREATEBY=result[2][0],
                           birthday=request.form['birthday']
                           )


# 回归收集信息界面-员工
@app.route("/goback1", methods=['GET', 'post'])
def gb1():
    # data = json.loads(request.get_data())
    name = request.form['username']
    gender = request.form['gender']
    age = request.form['age']
    phone = request.form['phone']
    id_card = request.form['id_card']
    birthday = request.form['birthday']

    global flag
    flag = "已完成采集"
    print(flag)
    # return render_template('start.html')
    # runfacecollect()
    return render_template('start1.html', flag="已完成采集", username= request.form['username'],
                           gender=request.form['gender'],
                           age=request.form['age'],
                           phone=request.form['phone'],
                           id_card=request.form['id_card'],
                           CREATEBY=result[2][0],
                           birthday=request.form['birthday'],
                           )

# 回归收集信息界面-义工
@app.route("/goback3", methods=['GET', 'post'])
def gb3():
    # data = json.loads(request.get_data())
    name = request.form['username']
    gender = request.form['gender']
    age = request.form['age']
    phone = request.form['phone']
    id_card = request.form['id_card']
    birthday = request.form['birthday']

    global flag
    flag = "已完成采集"
    print(flag)
    # return render_template('start.html')
    # runfacecollect()
    return render_template('start2.html', flag="已完成采集", username= request.form['username'],
                           gender=request.form['gender'],
                           age=request.form['age'],
                           phone=request.form['phone'],
                           id_card=request.form['id_card'],
                           CREATEBY=result[2][0],
                           birthday=request.form['birthday'],
                           )


# 回归收集信息界面-老人
@app.route("/goback2", methods=['GET', 'post'])
def gb2():
    # data = json.loads(request.get_data())
    name = request.form['username']
    gender = request.form['gender']
    age = request.form['age']
    phone = request.form['phone']
    id_card = request.form['id_card']
    birthday = request.form['birthday']

    global flag
    flag = "已完成采集"
    print(flag)
    # return render_template('start.html')
    # runfacecollect()
    return render_template('start.html', flag="已完成采集", username= request.form['username'],
                           gender=request.form['gender'],
                           age=request.form['age'],
                           phone=request.form['phone'],
                           id_card=request.form['id_card'],
                           CREATEBY=result[2][0],
                           birthday=request.form['birthday'],
                           firstguardian_name=request.form['firstguardian_name'],
                           firstguardian_relationship=request.form['firstguardian_relationship'],
                           firstguardian_phone=request.form['firstguardian_phone'],
                           )

@app.route("/modifyPassword", methods=['post', 'GET'])
def gomodifyP():
    return render_template("modifypassword.html")


@app.route("/modifyP", methods=['post', 'GET'])
def modifyP():
    ID = result[2][0]
    password = request.form['password']
    password2 = request.form['password2']
    if (password != password2):
        flash("两次密码不一致")
        return render_template("modifypassword.html")
    user1 = user.user()
    user1.modify(ID, password)

    return render_template("teacher_index.html")

# 刷新数据表格
@app.route("/freshdata", methods=['GET', 'post'])
def freshdata1():
    u = user.user()
    # data = json.loads(request.get_data())
    type = request.form['sd']
    print(type)
    return render_template("showCData.html", olddata=getold(), employdata=getEmp(), volundata=getVol(), info=getEvent())


# 主函数
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5001)
