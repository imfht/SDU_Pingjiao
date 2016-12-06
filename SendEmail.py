# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
MAILADD = "fiht@qq.com"
PASSWORD = 'duoewxgezorrbgec'

def sendEmail(toAdd, htmlText):
    subject=u'一键评价结果通知(╭￣3￣)╭♡'
    strFrom=MAILADD
    strTo = toAdd;
    msg = MIMEText(htmlText,_charset='utf-8')
    msg['Content-Type'] = 'Text/HTML'
    msg['Subject'] = Header(subject, 'utf-8')
    msg['To'] = strTo
    msg['From'] = MAILADD

    smtp = smtplib.SMTP_SSL('smtp.qq.com',465)
    smtp.login(MAILADD, password=PASSWORD)
    try:
        smtp.sendmail(strFrom, strTo, msg.as_string())
    finally:
        smtp.close;


if __name__ == "__main__":
    text ="邮件发送测试"
    sendEmail(MAILADD,text)

