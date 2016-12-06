#coding: utf8
import redis
from pingjia import Util
import threading
import time
from SendEmail import sendEmail
r = redis.Redis()


def run(name):
    while(1):
        item = r.blpop('class_info')
        print '%d接收到一个任务' % name
        xh,password,email = item[1].split('|')
        try:
            Util(xh,password,email).run()
        except Exception as e:
            print e
            sendEmail('fiht@qq.com',htmlText=str(e))
        print '%d完成到一个任务' % name

if __name__ == '__main__':
    threads = [threading.Thread(target=run,args=(i,)) for i in range(1,5)]

    for i in threads:
        i.start()
