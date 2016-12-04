# coding: utf-8

from urlparse import parse_qs
import sys
import random
import logging
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from SendEmail import sendEmail

wordsList = ['老师工作十分认真负责',
             '上课的时候很幽默',
             '就是作业有点多',
             '老师长得很好看呀~~最喜欢他的课了~~',
             '这个老师是我的老乡==',
             '这是我见过的PPT做的最用心的老师,给老师点各赞',
             '老师讲课突出重点，内容详细，条理清晰，细致入微',
             '老师很关心我们~~'
]
header = {'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)',
          'X-Requested-With': 'XMLHttpRequest',
          'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'zh-CN,zh;q=0.8'
          }

class Util():
    def __init__(self, xh, passwd, email=None):
        self.xh = xh
        self.passwd = passwd
        self.email = email
        print '开始任务%s'%self.xh
        self.s = requests.Session()
        if not self._loginTest():
            print '用户名或密码错误'
            return
        else:
            print '登录成功,正在获取课程数据...'
        self.info = self._getInfo()
        if len(self.info):
            print '成功获取课程数据，一共%s 门未提交的课程，准备提交评价'%len(self.info)
        else:
            print '已经评价完毕，请不要重复提交'
        self._postData()
        print '课程全部评估完毕，我们明年再见！'

        if self.email:
            self._sendEmail()
    def _sendEmail(self): # 发送邮件提醒
        text = '亲爱的%s:<br>你提交的课程评价已经完成，为了确保成功，请务必访问<a href="http://202.194.15.33:21043">http://202.194.15.33:21043</a> 查看是否评价成功，如果可以的话，希望你能够专注一下本猿的公众号，手动搜索 > 序猿的小站<br>' \
                '如果在课程评估中出现了什么问题，你可以通过这个邮件来联系我<br>' \
               '希望你是一个漂亮的小姑娘( ♥д♥)'%(self.xh)
        sendEmail(toAdd=self.email,htmlText=text)

    def _postData(self): # 评价课程
        py = random.choice(wordsList)
        base_data = u'xnxq=2016-2017-1&%s&wjid=1&wjmc=山东大学课堂教学评价&zbid=36&zblx=选择&zbda_0=5.0&zbid=37&zblx=选择&zbda_1=5.0&zbid=38&zblx=选择&zbda_2=5.0&zbid=39&zblx=选择&zbda_3=5.0&zbid=40&zblx=选择&zbda_4=5.0&zbid=41&zblx=选择&zbda_5=5.0&zbid=42&zblx=选择&zbda_6=5.0&zbid=43&zblx=选择&zbda_7=5.0&zbid=44&zblx=选择&zbda_8=5.0&zbid=45&zblx=选择&zbda_9=5.0&zbid=46&zblx=选择&zbda_10=5.0&zbid=47&zblx=选择&zbda_11=5.0&zbid=48&zblx=选择&zbda_12=5.0&zbid=49&zblx=选择&zbda_13=5.0&zbid=50&zblx=选择&zbda_14=5.0&zbid=51&zblx=选择&zbda_15=5.0&zbid=52&zblx=选择&zbda_16=4.0&zbid=53&zblx=选择&zbda_17=5.0&zbid=54&zblx=选择&zbda_18=4.0&zbid=55&zblx=选择&zbda_19=5.0&zbid=56&zblx=主观选择&zbda_20=推荐&zbid=57&zblx=主观&zbda_21='+py
        post_url = 'http://202.194.15.33:21043/b/pg/xs/add'
        for i in self.info:
            try:
                response = self.s.post(post_url, data=parse_qs(base_data % (i)), headers=header)
            except Exception as e:
                print e
                continue
            if 'success' not in response.text:
                print '程序异常，以下是Debug日志'
                print self.xh, self.passwd, response.text
                text = "抱歉,你的学号已经登录成功了但是服务器返回了异常数据,出于隐私的尊重我没有留下你的帐号密码,如果可以的话,我想请求一下你的帐号使用权,去Debug找到问题存在的地方,为更多同学谋求便利,谢谢!(同意捐赠帐号请回复学号 密码到此邮件,人品保证不泄漏任何隐私信息."
                sendEmail(toAdd=self.email,htmlText=text)
                continue
            else:
                print '成功评价一门课程，还剩下大概%ｓ门课程'

    def _getInfo(self): # 获取课程序列
        response = self.s.post('http://202.194.15.33:21043/b/pg/xs/list', data={
            'aoData': '[{"name":"sEcho","value":1},{"name":"iColumns","value":5},{"name":"sColumns","value":""},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":-1},{"name":"mDataProp_0","value":"kch"},{"name":"mDataProp_1","value":"kcm"},{"name":"mDataProp_2","value":"jsm"},{"name":"mDataProp_3","value":"function"},{"name":"mDataProp_4","value":"function"},{"name":"iSortCol_0","value":0},{"name":"sSortDir_0","value":"asc"},{"name":"iSortingCols","value":1},{"name":"bSortable_0","value":true},{"name":"bSortable_1","value":false},{"name":"bSortable_2","value":false},{"name":"bSortable_3","value":false},{"name":"bSortable_4","value":false}]'}, \
                               headers=header
                               ).json()
        return ['kch=%s&jsh=%s' % (i['kch'], i['jsh']) for i in response['object']['aaData'] if i['pgcs']==0]


    def _loginTest(self):
        try:
            response = self.s.post('http://202.194.15.33:21043/b/ajaxLogin',
                                   data={'j_username': self.xh, 'j_password': self.passwd}, headers=header)
            if 'success' in response.text:
                return True
            elif u'用户名或密码错误' in response.text:
                sendEmail(self.email,'很遗憾，你的登录密码错误，请仔细核对，你输入的密码是%s'%self.passwd)
                return False
            else:
                logging.log(level=5,msg='不能读懂服务器返回了什么')
        except requests.exceptions.Timeout:
            logging.log(level=5, msg='连接服务器失败')
            sendEmail(subject='Log 收集', htmlText='连接服务器失败，请人肉过来运维')

if __name__ == '__main__':
    logo = 'Life Need Dinner -by Fiht'
    print logo
    Util('UserID', 'PASSWD',email='fiht@qq.com')
