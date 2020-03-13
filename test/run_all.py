# coding=utf-8

import unittest
import os
import time
from util import HTMLTestRunner
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def discover_case():
    """加载所有测试用例"""
    basepath = os.path.relpath(os.path.dirname(__file__))
    casedir = os.path.join(basepath, 'cases')
    pattern = 'test*.py'
    discover = unittest.defaultTestLoader.discover(casedir, pattern)
    print(discover)
    return discover


def get_report_file(report_path):
    '''第三步：获取最新的测试报告'''
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    print(u'最新测试生成的报告： '+lists[-1])
    # 找到最新生成的报告文件
    report_file = os.path.join(report_path, lists[-1])
    return report_file


def send_mail(sender, psw, receiver, smtpserver, report_file, port):
    '''第四步：发送最新的测试报告内容'''
    with open(report_file, "rb") as f:
        mail_body = f.read()
    # 定义邮件内容
    msg = MIMEMultipart()
    body = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    msg['Subject'] = u"自动化测试报告"
    msg["from"] = sender
    msg["to"] = ",".join(receiver)     # 只能字符串
    msg.attach(body)
    # 添加附件
    att = MIMEText(open(report_file, "rb").read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment; filename= "report.html"'
    msg.attach(att)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)                      # 连服务器
        smtp.login(sender, psw)
    except:
        smtp = smtplib.SMTP_SSL(smtpserver, port)
        smtp.login(sender, psw)                       # 登录
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('test report email has send out !')

if __name__ == '__main__':
    # runner = unittest.TextTestRunner()
    # runner.run(discover_case())
    time = time.strftime('%Y%m%d%H%M%S')
    baseDir = os.path.relpath(os.path.dirname(__file__))
    reportDir = os.path.join(baseDir, 'report', 'report{}.html'.format(time))
    fp = open(reportDir, 'wb')
    title = '测试报告'
    description = '测试说明情况'
    runner = HTMLTestRunner.HTMLTestRunner(fp, verbosity=2, title=title, description=description)
    runner.run(discover_case())

    # # 获取最新的测试报告文件 没有使用
    report_file = get_report_file(os.path.join(baseDir, 'report'))  # 3获取最新的测试报告
    # #邮箱配置  邮箱配置可以写到yaml文件
    sender = "123456"
    psw = "123456"  # QQ邮箱授权码
    smtp_server = "smtp.exmail.qq.com"
    port = 465
    receiver = ["123@123.com.cn"]  # 单个收件人 list
    # receiver = ["yoyo@qq.com", "yoyoxxxx@qq.com"]  # 多个收件人

    # send_mail(sender, psw, receiver, smtp_server, reportDir, port)  # 4最后一步发送报告
