import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import configData
from common import configHttp as ConfigHttp

test_xls = configData.get_xls("userCase.xlsx", "login")

xls_params = configData.get_params_xls("userCase.xlsx", "login")

localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*test_xls)
class Login(unittest.TestCase):

    def setParameters(self, *params):
        self.par = xls_params
        self.list_parms = list(params)
        # get case_name，method，msg
        self.case_name = str(self.list_parms[0])
        self.method = str(self.list_parms[1])
        # bulid te request data
        self.dt_parm = dict(zip(self.par, self.list_parms))
        # delete the case_name, method, msg
        del self.dt_parm['case_name']
        del self.dt_parm['method']
        del self.dt_parm['msg']

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
        print(self.case_name + " Readly to start testing\n")

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

        # test interface
        print("step 4：请求方法：" + self.method)

        if self.method == 'get':
            configHttp.set_params(self.dt_parm)
            print("step 3：设置发送请求的参数：" + str(configHttp.params))
            self.response = configHttp.get()
        elif self.method == 'post':
            configHttp.set_data(self.dt_parm)
            print("step 3：设置发送请求的参数：" + str(configHttp.data))
            self.response = configHttp.post()

        # check result
        self.checkResult()
        print("step 5：检查结果\n")

    # def tearDown(self):
    #     """
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

        # if self.result == '0':
        #     email = configData.get_value_from_return_json(self.info, 'member', 'email')
        #     self.assertEqual(self.info['code'], self.code)
        #     self.assertEqual(self.info['msg'], self.msg)
        #     self.assertEqual(email, self.email)
        #
        # if self.result == '1':
        #     self.assertEqual(self.info['code'], self.code)
        #     self.assertEqual(self.info['msg'], self.msg)


if __name__ == '__main__':
    login_test = Login()
