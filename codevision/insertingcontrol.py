# -*- coding: utf-8 -*-
'''
将事件插入数据库的控制程序-控制 seconds 秒可插入1次

用法：
'''
import time
stop_threads=False #是否退出线程
#经过seconds秒可再次插入
def controltime(seconds):
    while True:
        f = open('codevision/allowinsertdatabase1.txt', 'r')
        content = f.read()
        f.close()

        is_allowed = content[11:12]
        if stop_threads:
            break
        if is_allowed == '0':
            print( '[检测陌生人和表情]-状态：不允许插入')
            for i in range(seconds, 0, -1):
                print('[检测陌生人和表情]-wait %d seconds...' % (i))
                time.sleep(1)

            f = open('codevision/allowinsertdatabase1.txt', 'w')
            f.write('is_allowed=1')
            f.close()
        elif is_allowed=='1':
            time.sleep(1)
        else:
            # print('pass')
            pass