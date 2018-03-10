import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import configData
from common import configHttp as ConfigHttp

login_xls = configData.get_xls("userCase.xlsx", "login")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, username, password, checkcode, code, data, msg):
        """
        set params
        :param case_name:
        :param method:
        :param username:
        :param password:
        :param checkcode
        :param code:
        :param data:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.username = str(username)
        self.password = str(password)
        self.checkcode = str(checkcode)
        self.code = str(code)
        self.data = str(data)
        self.msg = str(msg)
        self.response = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + " Readly to start testing")

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = configData.get_url_from_xml('login')
        configHttp.set_url(self.url)
        print("step 1：设置url  " + configHttp.url)

        # get visitor token
        # if self.token == '0':
        #     token = localReadConfig.get_headers("token_v")
        # elif self.token == '1':
        #     token = None

        # get headers and # set headers
        headers = localReadConfig.get_headers("content-Type")

        header = {"content-Type": str(headers)}
        configHttp.set_headers(header)
        print("step 2：设置header")

        # set params
        data = {"username": self.username, "password": self.password, "checkCode": self.checkcode}
        configHttp.set_data(data)
        print("step 3：设置发送请求的参数" + str(configHttp.data))

        # test interface
        self.response = configHttp.post()
        print(self.response.json())
        # method = str(self.return_json.request)[
        #          int(str(self.return_json.request).find('[')) + 1:int(str(self.return_json.request).find(']'))]
        # print("第四步：发送请求\n\t\t请求方法：" + method)

        # check result

        self.checkResult()
        print("第五步：检查结果")

    # def tearDown(self):
    #     """
    #
    #     :return:
    #     """
    #     info = self.info
    #     if info['code'] == 0:
    #         # get uer token
    #         token_u = configData.get_value_from_return_json(info, 'member', 'token')
    #         # set user token to config file
    #         localReadConfig.set_headers("TOKEN_U", token_u)
    #     else:
    #         pass
    #     self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])
    #     print("测试结束，输出log完结\n\n")
    #
    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.response.json()
        # show return message
        configData.show_return_msg(self.response)

        if self.result == '0':
            email = configData.get_value_from_return_json(self.info, 'member', 'email')
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            self.assertEqual(email, self.email)

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)


if __name__ == '__main__':
    login_test = Login()
    login_test.testLogin()
