import pymysql
import rsacrypt
import rsa
import datetime
cursor = None
db = None

class user:
    def connect_mysql(self):
        global cursor
        global db
        db = pymysql.connect(host='bj-cynosdbmysql-grp-94ctk06s.sql.tencentcdb.com', port=21171, user='root',
                             password='Stz123456', database='careOld')
        cursor = db.cursor()

    def login(self, userName, password):
        self.connect_mysql()
        global cursor
        sql = "select * from sys_user where UserName = '" + userName + "';"
        cursor.execute(sql)
        # 执行sql语句
        # 取一行结果
        result = cursor.fetchone()

        info = {}
        if result is None:
            info[0] = 0
            info[1] = "该用户未注册"
            return info
        sql1 = "select * from rsa where UserName = '" + userName + "';"
        cursor.execute(sql1)
        result1 = cursor.fetchone()
        pubkey = rsa.PublicKey(result1[2], result1[3])
        prikey = rsa.PrivateKey(int(result1[2]), int(result1[3]), int(result1[4]), int(result1[5]), int(result1[6]))
        rs_obj = rsacrypt.rsacrypt(pubkey, prikey)
        data = rs_obj.decrypt(result[4]).decode("utf - 8")
        if password == data:
            info[0] = 1
            info[1] = "登陆成功"
            info[2] = result
            return info
        else:
            info[0] = 0
            info[1] = "密码错误"
            return info

    def query(self, id):
        self.connect_mysql()
        global cursor
        sql = "select * from sys_user where ID = " + id + ";"
        cursor.execute(sql)
        # 执行sql语句
        # 取一行结果
        result = cursor.fetchone()
        info = {}
        info[0] = 1
        info[1] = result
        return info

    def queryAll(self):
        self.connect_mysql()
        global cursor
        info = {}
        sql = "select * from sys_user;"
        cursor.execute(sql)
        # 取一行结果
        result = cursor.fetchall()
        info[0] = 1
        i = 1
        for fetchInfo in result:
            info[i] = fetchInfo
            i = i + 1
        return info

    def eventStatistics(self):
        self.connect_mysql()
        global cursor
        global db
        info = {}
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        now1 = datetime.datetime.strptime(now, "%Y-%m-%d")  # 浠婂ぉ
        now0 = now1 + datetime.timedelta(days=1)  # 鏄庡ぉ
        now2 = now1 + datetime.timedelta(days=-1)  # 鏄ㄥぉ
        now3 = now1 + datetime.timedelta(days=-2)
        now4 = now1 + datetime.timedelta(days=-3)
        now5 = now1 + datetime.timedelta(days=-4)
        now6 = now1 + datetime.timedelta(days=-5)
        now7 = now1 + datetime.timedelta(days=-6)
        format = "%Y-%m-%d %H:%M:%S"

        sql0 = "select count(event_type = 0 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as emotion" \
               ", count(event_type = 1 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as interaction" \
               ", count(event_type = 2 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as stranger" \
               ", count(event_type = 3 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as fall" \
               ", count(event_type = 4 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as Invade  FROM event_info"
        var0 = (format, now6, format, now7, format, now6, format, now7, format, now6, format, now7, format, now6, format
                , now7, format, now6, format, now7)
        cursor.execute(sql0, var0)
        result0 = cursor.fetchone()

        sql1 = "select count(event_type = 0 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as emotion" \
               ", count(event_type = 1 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as interaction" \
               ", count(event_type = 2 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as stranger" \
               ", count(event_type = 3 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as fall" \
               ", count(event_type = 4 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as Invade  FROM event_info"
        var1 = (format, now5, format, now6, format, now5, format, now6, format, now5, format, now6, format, now5, format
                , now6, format, now5, format, now6)
        cursor.execute(sql1, var1)
        result1 = cursor.fetchone()
        # result1[5] = now6.strftime("%Y-%m-%d")

        sql2 = "select count(event_type = 0 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as emotion" \
               ", count(event_type = 1 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as interaction" \
               ", count(event_type = 2 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as stranger" \
               ", count(event_type = 3 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as fall" \
               ", count(event_type = 4 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as Invade  FROM event_info"
        var2 = (format, now4, format, now5, format, now4, format, now5, format, now4, format, now5, format, now4, format
                , now5, format, now4, format, now5)
        cursor.execute(sql2, var2)
        result2 = cursor.fetchone()
        # result2[5] = now5.strftime("%Y-%m-%d")

        sql3 = "select count(event_type = 0 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as emotion" \
               ", count(event_type = 1 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as interaction" \
               ", count(event_type = 2 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as stranger" \
               ", count(event_type = 3 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as fall" \
               ", count(event_type = 4 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as Invade  FROM event_info"
        var3 = (format, now3, format, now4, format, now3, format, now4, format, now3, format, now4, format, now3, format
                , now4, format, now3, format, now4)
        cursor.execute(sql3, var3)
        result3 = cursor.fetchone()
        # result3[5] = now4.strftime("%Y-%m-%d")

        sql4 = "select count(event_type = 0 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as emotion" \
               ", count(event_type = 1 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as interaction" \
               ", count(event_type = 2 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as stranger" \
               ", count(event_type = 3 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as fall" \
               ", count(event_type = 4 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as Invade  FROM event_info"
        var4 = (format, now2, format, now3, format, now2, format, now3, format, now2, format, now3, format, now2, format
                , now3, format, now2, format, now3)
        cursor.execute(sql4, var4)
        result4 = cursor.fetchone()
        # result4[5] = now3.strftime("%Y-%m-%d")

        sql5 = "select count(event_type = 0 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as emotion" \
               ", count(event_type = 1 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as interaction" \
               ", count(event_type = 2 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as stranger" \
               ", count(event_type = 3 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as fall" \
               ", count(event_type = 4 AND DATE_FORMAT( event_date, %s ) < %s " \
               "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as Invade  FROM event_info"
        var5 = (format, now1, format, now2, format, now1, format, now2, format, now1, format, now2, format, now1, format
                , now2, format, now1, format, now2)
        cursor.execute(sql5, var5)
        result5 = cursor.fetchone()
        # result5[5] = now2.strftime("%Y-%m-%d")

        sql = "select count(event_type = 0 AND DATE_FORMAT( event_date, %s ) < %s " \
              "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as emotion" \
              ", count(event_type = 1 AND DATE_FORMAT( event_date, %s ) < %s " \
              "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as interaction" \
              ", count(event_type = 2 AND DATE_FORMAT( event_date, %s ) < %s " \
              "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as stranger" \
              ", count(event_type = 3 AND DATE_FORMAT( event_date, %s ) < %s " \
              "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as fall" \
              ", count(event_type = 4 AND DATE_FORMAT( event_date, %s ) < %s " \
              "AND DATE_FORMAT( event_date, %s ) >= %s OR NULL) as Invade  FROM event_info"
        var = (format, now0, format, now1, format, now0, format, now1, format, now0, format, now1, format, now0, format
               , now1, format, now0, format, now1)
        cursor.execute(sql, var)
        result6 = cursor.fetchone()
        # result6[5] = now1.strftime("%Y-%m-%d")

        db.commit()
        info[0] = 1
        info[1] = "鏃堕棿缁熻鎴愬姛"
        info[2] = now7.strftime("%Y-%m-%d")
        info[3] = result0
        info[4] = now6.strftime("%Y-%m-%d")
        info[5] = result1
        info[6] = now5.strftime("%Y-%m-%d")
        info[7] = result2
        info[8] = now4.strftime("%Y-%m-%d")
        info[9] = result3
        info[10] = now3.strftime("%Y-%m-%d")
        info[11] = result4
        info[12] = now2.strftime("%Y-%m-%d")
        info[13] = result5
        info[14] = now1.strftime("%Y-%m-%d")
        info[15] = result6
        return info

    def modify(self, ID, password):
        self.connect_mysql()
        global cursor
        global db
        pubkey, prikey = rsa.newkeys(256)
        rs_obj = rsacrypt.rsacrypt(pubkey, prikey)
        newPassword = rs_obj.encrypt(password)
        info = {}
        updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql1 = "update sys_user set Password = %s , UPDATED = %s , UPDATEBY = %s where ID = %s"
        var1 = (newPassword, updated, ID, ID)
        cursor.execute(sql1, var1)
        sql2 = "update rsa a,sys_user b set a.n = %s , a.e = %s , a.d = %s , a.p = %s , a.q = %s where " \
               "a.UserName = b.UserName and b.ID = %s;"
        var2 = (prikey.n, prikey.e, prikey.d, prikey.p, prikey.q, ID)
        cursor.execute(sql2, var2)
        db.commit()
        info[0] = 1
        info[1] = "信息修改成功"
        return info
    # def register(self, userName, password, real_name, sex, email, phone):
    #     self.connect_mysql()
    #     global cursor
    #     info = {}
    #     sql = "select * from sys_user where UserName = '" + userName + "';"
    #     cursor.execute(sql)
    #     result1 = cursor.fetchall()
    #     print(result1)
    #     if len(result1) == 1:
    #         info[0] = 0
    #         info[1] = "账号已存在"
    #         return info
    #     else:
    #         sql = "insert into sys_user(UserName, Password, REAL_NAME, SEX, EMAIL, PHONE) values (%s, %s, %s, %s,%s)"%\
    #               (userName, password, real_name, sex, email, phone)
    #         # sql = "insert into sys_user(UserName, Password, REAL_NAME, SEX, EMAIL, PHONE) values ('" + userName \
    #         #        + "','" + password + "','" + real_name + "','" + sex + "','" + email + "','" + phone + "');"
    #         print(sql)
    #         cursor.execute(sql)
    #         info[0] = 1
    #         info[1] = "注册成功"
    #         return info

