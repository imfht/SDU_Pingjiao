# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
PASSWORD = 'xxxxx'

def sendEmail(htmlText,fromAdd='nofiht@qq.com', toAdd='fiht@qq.com', subject=u'一键评价结果通知(╭￣3￣)╭♡'):
    strFrom = fromAdd;
    strTo = toAdd;
    msg = MIMEText(htmlText,_charset='utf-8');
    msg['Content-Type'] = 'Text/HTML';
    msg['Subject'] = Header(subject, 'utf-8');
    msg['To'] = strTo;
    msg['From'] = strFrom;

    smtp = smtplib.SMTP_SSL('smtp.qq.com',465);
    smtp.login('nofiht@qq.com', password=PASSWORD);
    try:
        smtp.sendmail(strFrom, strTo, msg.as_string());
    finally:
        smtp.close;


if __name__ == "__main__":
    text = '亲爱的%s,你提交的课程评价已经完成，为了确保成功，请务必访问 http://202.194.15.33:21043 查看，如果可以的话，希望你能够专注一下本猿的公众号，手动搜索 > 序猿的小站' \
           '如果在课程评估中出现了什么问题，你可以通过这个邮件来联系我' \
           '希望你是一个漂亮的小姑娘( ♥д♥)' % (123)
    sendEmail(text)