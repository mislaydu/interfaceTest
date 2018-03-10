import unittest
import os
from common.Log import MyLog as Log
import readConfig as readConfig
from common.configEmail import MyEmail
import common.HTMLTestRunner as HTMLTestRunner

localReadConfig = readConfig.ReadConfig()


class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_result_path()
        on_off = localReadConfig.get_email("on_off")
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        self.caseFile = os.path.join(readConfig.proDir, "testCase")
        self.caseList = []
        self.email = MyEmail.get_email()

    # set running testcase
    def set_case_list(self):

        fb = open(self.caseListFile)

        for value in fb.readline():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))

            fb.close()

    # set case suit
    def set_case_suit(self):
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_model = []

        for case in self.caseList:
            # set case files
            case_file = os.path.join(readConfig.proDir, "testCase")
            print(case_file)
            case_name = case.split("/")[-1]
            print(case_name + ".py")
            discover = unittest.defaultTestLoader.discover(case_file, pattern=case_name + '.py', top_level_dir=None)
            suite_model.append(discover)

            if len(suite_model) > 0:
                for suite in suite_model:
                    for test_name in suite:
                        test_suite.addTest(test_name)
            else:
                return None
        return test_suite

    def run(self):
        try:
            suit = self.set_case_suite()
            if suit is not None:
                logger.info("********TEST START********")
                fp = open(resultPath, 'wb')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))

        finally:
            logger.info("*********TEST END*********")

            # send test report by eamil

            if int(on_off) == 0:
                self.email.send_email()
            elif int(on_off) == 1:
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    obj = AllTest()
    obj.run()
