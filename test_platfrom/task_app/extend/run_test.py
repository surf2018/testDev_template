import requests
import json
from ddt import ddt, data, unpack, file_data
import unittest
import csv
import requests
# from test_platfroms.common import response_succeess,response_failed
from task_app.apps import TASK_PATH, TASK_RUN_PATH, REPORT_PATH
import xmlrunner
import sys


# 测试数据
# 取文件
def get_file():
    taskid = sys.argv[1]
    path = TASK_PATH + '/task_' + taskid + ".json"
    return path


@ddt
class ccaSystem(unittest.TestCase):
    # def setUp(self):
    #     print("")
    # @data(*get_data("test_data.csv"))
    @file_data(TASK_PATH + "/task.json")
    @unpack
    def test_run(self, url, method, type, header, data, assertText):
        try:
            header = json.loads(header)
            data = json.loads(data)
            if (method == 'post'):
                if (type != 'json'):
                    # 非json数据
                    try:
                        if ('file' in data.keys()):
                            response = requests.post(url, files=data)
                            # print(response)
                        else:
                            # data=json.loads(data)
                            response = requests.post(url, data=data, headers=header)
                            # print("post" +
                            #       response.text +
                            #       "status code:" +
                            #       str(response.status_code))
                            if (assertText == ""):
                                if (response.status_code == 200):
                                    message = "OK"
                                else:
                                    message = "Fail"
                            else:
                                # print("assertText:"+assertText)
                                if (response.status_code == 200 and assertText in response.text):
                                    message = "OK"
                                else:
                                    message = "Fail"
                    except Exception as e:
                        print(e)
                        message="Fail"
                else:
                    # json数据
                    # print("post 请求json")
                    try:
                        data = json.dumps(data)
                        response = requests.post(url, data=data, headers=header)
                        # print("post" +
                        #       response.text +
                        #       "status code:" +
                        #       str(response.status_code))
                        if (assertText == ""):
                            if (response.status_code == 200):
                                message = "OK"
                            else:
                                message = "Fail"
                        else:
                            if (assertText in response.text):
                                message = "OK"
                            else:
                                message = "Fail"
                    except requests.exceptions.ConnectionError:
                        message = "Fail"
                        # print("Fail:Fail to establish a new connection.")
            elif (method == 'get'):
                # get 请求
                # print("get 请求")
                if (type != 'json'):
                    # print("type is not json")
                    try:
                        response = requests.get(url, params=data, headers=header)
                        # print("get方法获取reponse:" +
                        #       response.text +
                        #       "status code:" +
                        #       str(response.status_code))
                        if (assertText == ""):
                            if (response.status_code == 200):
                                message = "OK"
                            else:
                                message = 'Fail'
                        else:
                            # print("assertText:"+str(assertText))
                            if (assertText in response.text):
                                message = "OK"
                            else:
                                message = "Fail"
                    except requests.exceptions.MissingSchema:
                        message = "Fail"
                        # print("Fail:URL输入错误,No schema supplied.")
                    except json.decoder.JSONDecodeError:
                        message = "Fail"
                        # print("Fail:hearder或data非json格式")
                    except requests.exceptions.ConnectionError:
                        message = "Fail"
                        # print("Fail:Fail to establish a new connection.")
                else:
                    # print("type is json")
                    try:
                        data = json.dumps(data)
                        # print(data)
                        response = requests.get(url, params=data, headers=header)
                        # print("get方法获取返回值:" +
                        #       response.text +
                        #       "statu code:" +
                        #       str(response.status_code))
                        if (assertText == ''):
                            if (response.status_code == 200):
                                message = "OK"
                            else:
                                message = 'Fail'
                        else:
                            # print("assertText:"+str(assertText))
                            if (assertText in response.text):
                                message = "OK"
                            else:
                                message = "Fail"
                    except:
                        message = "Fail"
                        print("Fail")
                # return HttpResponse(response)
            else:
                message = "Fail"
                # print(message+"method 不是post 或者get")
            self.assertEqual(message, 'OK')
        except Exception as e:
            print(e)
            print("json解析失败")
            message="Fail"
            self.assertEqual(message,"OK")
    # def tearDown(self):
    #     print("")


def runTaskTestcase():
    filename = REPORT_PATH + '/taskResult.xml'
    # print(filename)
    with open(filename, 'w', encoding='utf-8') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output), failfast=False, buffer=False, catchbreak=False)


if __name__ == '__main__':
    # print("cmmd parameter:"+str(sys.argv[1]))
    # files=get_file()
    # print(files)
    runTaskTestcase()
