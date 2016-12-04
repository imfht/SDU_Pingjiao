# coding: utf-8
from flask import Flask
from flask import render_template
from flask import request
from threading import Thread
from pingjia import Util
from Queue import Queue
import redis
app = Flask(__name__)
que = Queue()
def run_Util():
    while(True):
        i = que.get()
        print 'Get a Item'
        Util(i[0],i[1],i[2])
r = redis.Redis()
@app.route('/',methods=['POST','GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        xh = request.form['xh']
        passwd = request.form['password']
        email = request.form['email']
        r.rpush('info','%s/%s/%s'%(xh,passwd,email))
        return u'<script>alert("提交完毕,请等待邮件通知,如果五分钟之内没有收到邮件,尝试重新提交(也可以找我反馈");window.close();</script>'

if __name__ == '__main__':
    app.run(port=5000,debug=True)
