import requests
import readConfig as readConfig
from common.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:
    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("host")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}

    # 设置请求的url
    def set_url(self, url):
        self.url = scheme + '://' + host + ':' + port + '/' + url

    def set_headers(self, header):
        self.headers = header

    def set_params(self, param):
        self.params = param

    def set_data(self, data):
        self.data = data

    def set_files(self, file):
        self.files = file

    # defined http get method
    def get(self):
        try:
            response = requests.get(self.url, params=self.params, headers=self.set_headers, timeout=float(timeout))
            # response.raise_for_status()
            response.enconding = "utf-8"
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None

    # defined http post method
    def post(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files,
                                     timeout=float(timeout))
            # response.raise_for_status()
            #  响应编码
            response.enconding = "utf-8"
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None



if __name__ == '__main__':
    testconf = ConfigHttp()
    testconf.set_url('Register/login/login.do')
    testconf.set_headers({'content-Type': 'application/x-www-form-urlencoded'})
    testconf.set_data({'username': 'buyer1', 'password': '0b66cc77759a4c6f29e460d4fa43c580', 'checkCode': 'S3rw0MdY'})
    res = testconf.post()
    print(res.text)

