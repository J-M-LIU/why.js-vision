import datetime

import pymysql

cursor = None
db = None


class old:
    def connect_mysql(self):
        global cursor
        global db
        db = pymysql.connect(host='', port=, user='',
                             password='', database='careOld')
        cursor = db.cursor()

    def addInfo(self, username, gender, age, phone, id_card, birthday, CREATEBY, firstguardian_name,
                firstguardian_relationship,
                firstguardian_phone):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql = "select * from oldperson_info where username = '" + username + "';"
        cursor.execute(sql)
        result1 = cursor.fetchall()
        if len(result1) == 1:
            info[0] = 0
            info[1] = "该老人信息已存在"
            return info
        else:
            created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql1 = "insert into oldperson_info(username, gender, age, phone, id_card, birthday, CREATED, CREATEBY" \
                   ", firstguardian_name, firstguardian_relationship, firstguardian_phone) " \
                   "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            var1 = (username, gender, age, phone, id_card, birthday, created, CREATEBY, firstguardian_name
                    , firstguardian_relationship, firstguardian_phone)
            cursor.execute(sql1, var1)
            db.commit()
            sql2 = "select ID from oldperson_info where username = %s and gender = %s and phone = %s and id_card = %s"
            var2 = (username, gender, phone, id_card)
            cursor.execute(sql2, var2)
            result2 = cursor.fetchone()
            info[0] = 1
            info[1] = "信息录入成功"
            info[2] = result2[0]#id
            return result2


    def addImage(self, ID, imgset_dir):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql1 = "update oldperson_info set imgset_dir = %s where ID = %s"
        var1 = (imgset_dir, ID)
        cursor.execute(sql1, var1)
        db.commit()
        info[0] = 1
        info[1] = "图像采集成功"
        return info


    #模糊查询
    def queryFuzzy(self, query):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        var = '%' + query + '%'
        sql1 = "select count(*) from oldperson_info where username like '%s'" % var
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        sql = "select * from oldperson_info where username like '%s'" % var
        cursor.execute(sql)
        result = cursor.fetchall()
        info[0] = 1
        info[1] = "老人信息模糊查询成功"
        info[2] = result1
        info[3] = result
        return info

    def queryAll(self):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql1 = "select count(*) from oldperson_info"
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        sql = "select * from oldperson_info"
        cursor.execute(sql)
        result = cursor.fetchall()
        info[0] = 1
        info[1] = "老人信息获取成功"
        info[2] = result1#总数
        info[3] = result
        return info

    # 删除老人
    def deleteOld(self, ID):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql = "delete from oldperson_info where ID = %s"
        var = (ID)
        cursor.execute(sql, var)
        db.commit()
        info[0] = 1
        info[1] = "老人信息删除成功"
        return info

    def modifyOld(self, ID, username, gender, age, phone, id_card, birthday, UPDATEBY, firstguardian_name
                  , firstguardian_relationship, firstguardian_phone):
        self.connect_mysql()
        global cursor
        global db
        updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info = {}
        sql = "update oldperson_info set username = %s, gender = %s ,age = %s, phone = %s, id_card = %s, birthday = %s" \
              ", UPDATED = %s, UPDATEBY = %s, firstguardian_name = %s, firstguardian_relationship = %s" \
              ", firstguardian_phone = %s where ID = %s"
        var = (username, gender, age, phone, id_card, birthday, updated, UPDATEBY, firstguardian_name
               , firstguardian_relationship, firstguardian_phone, ID)
        cursor.execute(sql, var)
        sql1 = "select count(*) from oldperson_info"
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        db.commit()
        info[0] = 1
        info[1] = "老人信息修改成功"
        info[2] = result1
        return info


    def ageStatistics(self):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql = "select count(age<60 OR NULL), count(age<70 and age>=60 OR NULL), count(age<80 and age>=70 OR NULL)" \
              ", count(age>=80 OR NULL) from oldperson_info"
        cursor.execute(sql)
        result = cursor.fetchall()
        info[0] = 1
        info[1] = "老人年龄统计成功"
        info[2] = result
        return info
