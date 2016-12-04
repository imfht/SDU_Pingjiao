#coding: utf8
import redis
from pingjia import Util
import threading
from SendEmail import sendEmail
r = redis.Redis()

def run(id):
    while(1):
        item = r.blpop('info')
        print '%d接收到一个任务' % id
        xh,passwd,email = item[1].split('/')
        try:
            Util(xh,passwd,email)
        except Exception as e:
            print e
            sendEmail('fiht@qq.com',htmlText=str(e))
        print '%d完成到一个任务' % id

if __name__ == '__main__':
    threads = [threading.Thread(target=run,args=(i,)) for i in range(1,5)]

    for i in threads:
        i.start()
