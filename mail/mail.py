import traceback
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header


class Mail:

    def __init__(self, from_user, password, smtp_server, smtp_port):
        self.from_user = from_user
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send(self, mail, title, msgtext):
        try:
            # 发信服务器
            # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
            msg = MIMEText(msgtext, 'plain', 'utf-8')
            # 邮件头信息
            msg['From'] = Header(self.from_user)
            # msg['From'] = Header(u'from Admin<{}>'.format(self.from_user), 'utf-8')
            msg['To'] = Header(mail)
            msg['Subject'] = Header(title, 'utf-8')
            # 开启发信服务，这里使用的是加密传输
            server = smtplib.SMTP_SSL(host=self.smtp_server)
            server.connect(self.smtp_server, self.smtp_port)
            # 登录发信邮箱
            server.login(self.from_user, self.password)
            # 发送邮件
            server.sendmail(self.from_user, mail, msg.as_string())
            # 关闭服务器
            server.quit()
        except Exception as e:
            print(traceback.format_exc())

    def send_html(self, mail, title, msgtext):
        try:
            # 发信服务器
            # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
            msg = MIMEText(msgtext, 'html', 'utf-8')
            # 邮件头信息
            msg['From'] = Header(self.from_user)
            # msg['From'] = Header(u'from Admin<{}>'.format(self.from_user), 'utf-8')
            msg['To'] = Header(mail)
            msg['Subject'] = Header(title, 'utf-8')
            # 开启发信服务，这里使用的是加密传输
            server = smtplib.SMTP_SSL(host=self.smtp_server)
            server.connect(self.smtp_server, self.smtp_port)
            # 登录发信邮箱
            server.login(self.from_user, self.password)
            # 发送邮件
            server.sendmail(self.from_user, mail, msg.as_string())
            # 关闭服务器
            server.quit()
        except Exception as e:
            print(traceback.format_exc())
