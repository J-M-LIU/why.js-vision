import pymysql
import datetime

cursor = None
db = None


class employee:
    def connect_mysql(self):
        global cursor
        global db
        db = pymysql.connect(host='bj-cynosdbmysql-grp-94ctk06s.sql.tencentcdb.com', port=21171, user='root',
                             password='Stz123456', database='careOld')
        cursor = db.cursor()

    def addInfo(self, username, gender, age, phone, id_card, birthday, CREATEBY):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql = "select * from employee_info where username = '" + username + "';"
        cursor.execute(sql)
        result1 = cursor.fetchall()
        if len(result1) == 1:
            info[0] = 0
            info[1] = "该工作人员信息已存在"
            return info
        else:
            created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql1 = "insert into employee_info(username, gender, age, phone, id_card, birthday, CREATED, CREATEBY) " \
                   "values (%s,%s,%s,%s,%s,%s,%s,%s)"
            var1 = (username, gender, age, phone, id_card, birthday, created, CREATEBY)
            cursor.execute(sql1, var1)
            db.commit()
            sql2 = "select ID from employee_info where username = %s and gender = %s and phone = %s and id_card = %s"
            var2 = (username, gender, phone, id_card)
            cursor.execute(sql2, var2)
            result2 = cursor.fetchone()
            info[0] = 1
            info[1] = "信息录入成功"
            info[2] = result2[0]
            return info

    def modifyEmployee(self, ID, username, gender, age, phone, id_card, birthday, UPDATEBY):
        self.connect_mysql()
        global cursor
        global db
        updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info = {}
        sql = "update employee_info set username = %s, gender = %s ,age = %s, phone = %s, id_card = %s, birthday = %s" \
              ", UPDATED = %s, UPDATEBY = %s where ID = %s"
        var = (username, gender, age, phone, id_card, birthday, updated, UPDATEBY, ID)
        cursor.execute(sql, var)
        db.commit()
        info[0] = 1
        info[1] = "工作人员信息修改成功"
        return info

    def addImage(self, ID, imgset_dir):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql1 = "update employee_info set imgset_dir = %s where ID = %s"
        var1 = (imgset_dir, ID)
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
        sql1 = "select count(*) from employee_info"
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        sql = "select * from employee_info"
        cursor.execute(sql)
        result = cursor.fetchall()
        info[0] = 1
        info[1] = "工作人员信息获取成功"
        info[2] = result1
        info[3] = result
        return info

    def deleteEmployee(self, ID):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql = "delete from employee_info where ID = %s"
        var = (ID)
        cursor.execute(sql, var)
        db.commit()
        info[0] = 1
        info[1] = "工作人员信息删除成功"
        return info

    def queryFuzzy(self, query):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        var = '%' + query + '%'
        sql1 = "select count(*) from employee_info where username like '%s'" % var
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        sql = "select * from employee_info where username like '%s'" % var
        cursor.execute(sql)
        result = cursor.fetchall()
        info[0] = 1
        info[1] = "工作人员信息模糊查询成功"
        info[2] = result1
        info[3] = result
        return info

    def ageStatistics(self):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        sql = "select count(age<30 OR NULL), count(age<40 and age>=30 OR NULL), count(age<50 and age>=40 OR NULL)" \
              ", count(age>=50 OR NULL) from employee_info"
        cursor.execute(sql)
        result = cursor.fetchall()
        info[0] = 1
        info[1] = "工作人员年龄统计成功"
        info[2] = result
        return info
