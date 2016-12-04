# coding: utf-8
from flask import Flask
from flask import render_template
from flask import request
from threading import Thread
from pingjia import Util
from Queue import Queue
app = Flask(__name__)
que = Queue()
def run_Util():
    while(True):
        i = que.get()
        print 'Get a Item'
        Util(i[0],i[1],i[2])

@app.route('/',methods=['POST','GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        xh = request.form['xh']
        passwd = request.form['password']
        email = request.form['email']
        que.put([xh,passwd,email])
        return u'请求已经成功提交，评价完毕之后将会发送邮件通知。'

if __name__ == '__main__':
    Thread(target=run_Util).start()
    app.run(port=5000)
