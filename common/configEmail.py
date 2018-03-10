import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import threading
import readConfig as readConfig
from common.Log import MyLog
import zipfile
import glob

localReadConfig = readConfig.ReadConfig()


class Email:
    def __init__(self):
        global host, user, password, port, sender, title, content
        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        title = localReadConfig.get_email("subject")
        content = localReadConfig.get_email("content")
        self.value = localReadConfig.get_email("content")
        self.receiver = []

        # get receiver list
        for n in str(self.value).split("/"):
            self.receiver.append(n)

        # defined email subject

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = title + " " + date
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        # 邮件类型为"multipart/mixed"的邮件包含附件
        self.msg = MIMEMultipart('mixed')

    def config_header(self):
        # 设置邮件主题
        self.msg['subject'] = self.subject
        # 发件人
        self.msg['from'] = sender
        # 收件人
        self.msg['to'] = "".join(self.receiver)

    def config_content(self):
        content_plain = MIMEText(content, 'plain', 'utf-8')
        self.msg.attach(content_plain)

    def config_file(self):
        # if the file content is not null, then config the email file

        if self.check_file():
            report_path = self.log.get_result_path()
            zip_path = os.path.join(readConfig.proDir, "result", "test.zip")

            # zip file
            files = glob.glob(report_path + '\*')
            f = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
            for file in files:
                f.write(file)
                f.close()

            report_file = open(zip_path, 'rb').read()
            # 构造html及附件
            file_html = MIMEText(report_file, 'base64', 'utf-8')
            file_html['Content-Type'] = 'application/octet-stream'
            file_html['Content-Disposition'] = 'attachment; filename="test.zip"'
            self.msg.attach(file_html)

    def check_file(self):
        report_path = self.log.get_result_path()
        if os.path.isfile(report_path) and not os.stat(report_path) == 0:
            return True
        else:
            return False

    def send_email(self):
        self.config_header()
        self.config_content()
        self.config_file()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(host)
            smtp.login(user, password)
            smtp.sendmail(sender, self.receiver.self.msg.as_string())
            smtp.quit()
            self.logger.info("The test report has send to developer by email.")
        except Exception as ex:
            self.logger.error(str(ex))


class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():
        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()

        return MyEmail.email


if __name__ == "__main__":
    email = MyEmail.get_email()
