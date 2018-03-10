import codecs
import os
import configparser

proDir = os.path.split(os.path.realpath(__file__))[0]
# 设置配置文件路径
configPath = os.path.join(proDir, "config.ini")


class ReadConfig:
    def __init__(self):
        conf = open(configPath)
        data = conf.read()

        # remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        conf.close()

        # 实例化configParser对象
        self.cf = configparser.ConfigParser()
        # 读取配置文件
        self.cf.read(configPath)

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self,name):
        value = self.cf.get("HEADERS",name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    # 基本的写入操作
    # 定义方法，修改config分组下指定name的值value
    def setConfigValue(self, name, value):
        cfg = self.cf.set("config", name, value)
        fp = open(r'config.ini', 'w')
        cfg.write(fp)
