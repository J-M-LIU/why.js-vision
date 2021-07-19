import pymysql
import datetime


cursor = None
db = None


class volunteer:
    def connect_mysql(self):
        global cursor
        global db
        db = pymysql.connect(host='bj-com', port=, user='root',
                             password='', database='careOld')
        cursor = db.cursor()

    def addInfo(self, name, gender, age, phone, id_card, birthday, CREATEBY):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql = "select * from volunteer_info where name = '" + name + "';"
        cursor.execute(sql)
        result1 = cursor.fetchall()
        if len(result1) == 1:
            info[0] = 0
            info[1] = "该义工信息已存在"
            return info
        else:
            created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql1 = "insert into volunteer_info(name, gender, age, phone, id_card, birthday, CREATED, CREATEBY) " \
                   "values (%s,%s,%s,%s,%s,%s,%s,%s)"
            var1 = (name, gender, age, phone, id_card, birthday, created, CREATEBY)
            cursor.execute(sql1, var1)
            db.commit()
            sql2 = "select ID from volunteer_info where name = %s and gender = %s and phone = %s and id_card = %s"
            var2 = (name, gender, phone, id_card)
            cursor.execute(sql2, var2)
            result2 = cursor.fetchone()
            info[0] = 1
            info[1] = "信息录入成功"
            info[2] = result2[0]
            return info

    def modifyVolunteer(self, ID, name, gender, age, phone, id_card, birthday, UPDATEBY):
        self.connect_mysql()
        global cursor
        global db
        updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info = {}
        sql = "update volunteer_info set name = %s, gender = %s ,age = %s, phone = %s, id_card = %s, birthday = %s" \
              ", UPDATED = %s, UPDATEBY = %s where ID = %s"
        var = (name, gender, age, phone, id_card, birthday, updated, UPDATEBY, ID)
        cursor.execute(sql, var)
        db.commit()
        info[0] = 1
        info[1] = "义工信息修改成功"
        return info

    def addImage(self, id, imgset_dir):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql1 = "update volunteer_info set imgset_dir = %s where ID = %s"
        var1 = (imgset_dir, id)
        cursor.execute(sql1, var1)
        db.commit()
        info[0] = 1
        info[1] = "图像采集成功"
        return info

    def queryAll(self):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql1 = "select count(*) from volunteer_info"
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        sql = "select * from volunteer_info"
        cursor.execute(sql)
        result = cursor.fetchall()
        info[0] = 1
        info[1] = "义工信息获取成功"
        info[2] = result1
        info[3] = result
        return info

    def deleteVolunteer(self, ID):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql = "delete from volunteer_info where ID = %s"
        var = (ID)
        cursor.execute(sql, var)
        db.commit()
        info[0] = 1
        info[1] = "义工信息删除成功"
        return info

    def queryFuzzy(self, query):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        var = '%' + query + '%'
        sql1 = "select count(*) from volunteer_info where name like '%s'" % var
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        sql = "select * from volunteer_info where name like '%s'" % var
        cursor.execute(sql)
        result = cursor.fetchall()
        info[0] = 1
        info[1] = "义工信息模糊查询成功"
        info[2] = result1
        info[3] = result
        return info

    def ageStatistics(self):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql = "select count(age<20 OR NULL), count(age<30 and age>=20 OR NULL), count(age<40 and age>=30 OR NULL)" \
              ", count(age>=40 OR NULL) from volunteer_info"
        cursor.execute(sql)
        result = cursor.fetchall()
        info[0] = 1
        info[1] = "义工年龄统计成功"
        info[2] = result
        return info
