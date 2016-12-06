# coding: utf-8

from urlparse import parse_qs
from SendEmail import sendEmail
from config import commentList, allCommentSuccessMsg, passwordErrorMsg, commentErrorMsg
import sys
import random
import requests
import logging
import getpass

reload(sys)
sys.setdefaultencoding('utf-8')

header = {'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)',
          'X-Requested-With': 'XMLHttpRequest',
          'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'zh-CN,zh;q=0.8'
          }


def init_logging(logger_name):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='./pingjia.log',
                        filemode='a+'
                        )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logger = logging.getLogger(logger_name)
    logger.addHandler(console)
    return logger


class Util:
    def __init__(self, xh, passwd, email=None):
        self.xh = xh
        self.password = passwd
        self.email = email
        self.s = requests.Session()
        self.class_info = []
        self.logger = init_logging(logger_name=self.xh)

    def run(self):
        print '开始任务%s' % self.xh
        if not self._login():
            self.logger.info('登录失败,使用密码 %s'%self.password)
            try:
                sendEmail(self.email, passwordErrorMsg % self.password)
            except Exception: # @todo 用户输入(没有邮箱帐号会很麻烦.
                pass
            return
        else:
            self.logger.info('%s 登录成功'%self.xh)
        self.class_info = self._get_class_info()
        if len(self.class_info):
            self.logger.info('获取到%s门课程' % len(self.class_info))
        else:
            self.logger.warning('提交了一个已经完成评估的课程')
        self._post_comment_data()
        self.logger.info('课程全部评估完毕')

        if self.email:
            self._send_success_email()
            self.logger.info('成功发送通知邮件%s'%self.email)

    def _send_success_email(self):  # 发送邮件提醒
        text = allCommentSuccessMsg % self.xh
        sendEmail(toAdd=self.email, htmlText=text)

    def _post_comment_data(self):  # 评价课程
        py = random.choice(commentList) # 评语
        base_data = u'xnxq=2016-2017-1&%s&wjid=1&wjmc=山东大学课堂教学评价&zbid=36&zblx=选择' \
                    u'&zbda_0=5.0&zbid=37&zblx=选择&zbda_1=5.0&zbid=38&zblx=选择&zbda_2=5.0&' \
                    u'zbid=39&zblx=选择&zbda_3=5.0&zbid=40&zblx=选择&zbda_4=5.0&zbid=41&zblx=' \
                    u'选择&zbda_5=5.0&zbid=42&zblx=选择&zbda_6=5.0&zbid=43&zblx=选择&zbda_7=5.0' \
                    u'&zbid=44&zblx=选择&zbda_8=5.0&zbid=45&zblx=选择&zbda_9=5.0&zbid=46&zblx=选择' \
                    u'&zbda_10=5.0&zbid=47&zblx=选择&zbda_11=5.0&zbid=48&zblx=选择&zbda_12=5.0' \
                    u'&zbid=49&zblx=选择&zbda_13=5.0&zbid=50&zblx=选择&zbda_14=5.0&zbid=51&zblx=选择' \
                    u'&zbda_15=5.0&zbid=52&zblx=选择&zbda_16=4.0&zbid=53&zblx=选择&zbda_17=5.0&zbid=54' \
                    u'&zblx=选择&zbda_18=4.0&zbid=55&zblx=选择&zbda_19=5.0&zbid=56&zblx=主观选择&zbda_20=推荐' \
                    u'&zbid=57&zblx=主观&zbda_21=' + py
        post_url = 'http://202.194.15.33:21043/b/pg/xs/add'
        for i in self.class_info:
            try:
                response = self.s.post(post_url, data=parse_qs(base_data % (i)), headers=header)
            except Exception as e:
                print e
                continue
            if 'success' not in response.text:
                print '程序异常，以下是Debug日志'
                print self.xh, self.password, response.text
                text = commentErrorMsg
                sendEmail(toAdd=self.email, htmlText=text)
                continue
            else:
                print '成功评价一门课程，还剩下大概%ｓ门课程'

    def _get_class_info(self):  # 获取课程序列
        response = self.s.post('http://202.194.15.33:21043/b/pg/xs/list', data={
            'aoData': '[{"name":"sEcho","value":1},{"name":"iColumns","value":5},{"name":"sColumns","value":""},'
                      '{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":-1},'
                      '{"name":"mDataProp_0","value":"kch"},{"name":"mDataProp_1","value":"kcm"},'
                      '{"name":"mDataProp_2","value":"jsm"},{"name":"mDataProp_3","value":"function"},'
                      '{"name":"mDataProp_4","value":"function"},{"name":"iSortCol_0","value":0},'
                      '{"name":"sSortDir_0","value":"asc"},{"name":"iSortingCols","value":1},'
                      '{"name":"bSortable_0","value":true},{"name":"bSortable_1","value":false},'
                      '{"name":"bSortable_2","value":false},{"name":"bSortable_3","value":false},'
                      '{"name":"bSortable_4","value":false}]'}, \
                               headers=header
                               ).json()
        return ['kch=%s&jsh=%s' % (i['kch'], i['jsh']) for i in response['object']['aaData'] if i['pgcs'] == 0]

    def _login(self):
        try:
            response = self.s.post('http://202.194.15.33:21043/b/ajaxLogin',
                                   data={'j_username': self.xh, 'j_password': self.password}, headers=header)
            if 'success' in response.text:
                return True
            elif u'用户名或密码错误' in response.text:
                return False
            else:
                self.logger.log(level=5, msg='不能读懂服务器返回了什么')
        except requests.exceptions.Timeout:
            self.logger.log(level=5, msg='连接服务器失败')
            sendEmail(subject='Log 收集', htmlText='连接服务器失败，请人肉过来运维')


if __name__ == '__main__':
    logo = 'Life Need Dinner -by Fiht'
    print logo
    userID = raw_input('请输入学号:\n')
    password = getpass.getpass('请输入选课密码\n')
    Util(userID, password, email=None).run()
