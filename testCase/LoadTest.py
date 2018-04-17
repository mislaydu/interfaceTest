from common import configData
from common import configHttp as ConfigHttp
from common import Log as Log
import readConfig as readConfig

localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()


def set_test_case(xls_name):
    xls_sheet = configData.get_xls_sheet(xls_name)
    for sh in xls_sheet:
        # 获取sheet的参数列表
        xls_params = configData.get_params_xls(xls_name, sh)
        # 获取参数sheet的所有参数值
        test_xls = configData.get_xls(xls_name, sh)
        for txl in test_xls:
            lt = LoadTest(sh, xls_params, *txl)
            # run test case
            lt.run_test()
        print("<--------------------Test " + sh + " Finsish-------------------->\n\n")


class LoadTest:

    def __init__(self, sh, xls_params, *params):
        self.sheetname = sh
        self.parm = xls_params
        self.list_parms = list(params)
        # get case_name，method，msg
        self.case_name = str(self.list_parms[0])
        self.method = str(self.list_parms[1])
        # bulid te request data
        self.dt_parm = dict(zip(self.parm, self.list_parms))
        # delete the case_name, method, msg
        del self.dt_parm['case_name']
        del self.dt_parm['method']
        del self.dt_parm['msg']

        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()

        self.url = None
        self.response = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def set_up(self):
        """
        :return:
        """
        print("Test case: " + self.case_name + " Readly to start testing\n")

    def run_test(self):
        """
        test body
        :return:
        """

        self.set_up()
        # set url
        self.url = configData.get_url_from_xml(self.sheetname)
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
        self.check_result()
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
    def check_result(self):
        """
        check test result
        :return:
        """
        if self.response.strip() == '':
            print("The response is Null")
        else:
            self.info = self.response.json()
        # show return message
        configData.show_return_msg(self.response)


if __name__ == '__main__':
    set_test_case("userCase.xlsx")
