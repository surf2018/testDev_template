
import requests
import json
from ddt import ddt,data,unpack,file_data
import unittest
import csv
import requests
# from test_platfroms.common import response_succeess,response_failed
from task_app.apps import TASK_PATH,TASK_RUN_PATH,REPORT_PATH
import xmlrunner
import sys
#测试数据
#取文件
def get_file():
    taskid=sys.argv[1]
    path = TASK_PATH + '/task_'+taskid+".json"
    return path

@ddt
class ccaSystem(unittest.TestCase):
    def setUp(self):
        print("running test task")
    # @data(*get_data("test_data.csv"))
    @file_data(TASK_PATH+"/task_1.json")
    @unpack
    def test_run(self,url,method,type,header,data,assertText):
        print(url,method)
        header=json.loads(header)
        data=json.loads(data)
        message=""
        if (method == 'post'):
            if (type != 'json'):
                if ('file' in data.keys()):
                    response = requests.post(url, files=data)
                    print(response)
                else:
                    response = requests.post(url, data=data, headers=header)
                    print("post" +
                          response.text +
                          "status code:" +
                          str(response.status_code))
                    if (assertText == ""):
                        if (response.status_code == '200'):
                            message = "OK"
                        else:
                            message = "Fail"
                    else:
                        if (assertText in response.text):
                            message = "OK"
                        else:
                            message="Fail"
            else:
                # json数据
                print("post 请求json")
                try:
                    data = json.dumps(data)
                    response = requests.post(url, data=data, headers=header)
                    print("post" +
                          response.text +
                          "status code:" +
                          str(response.status_code))
                    if(assertText==""):
                        if(response.status_code=='200'):
                            message="OK"
                        else:
                            message="Fail"
                    else:
                        if(assertText in response.text):
                            message="OK"
                        else:
                            message="Fail"
                except requests.exceptions.ConnectionError:
                    message = "Fail"
                    print("Fail:Fail to establish a new connection.")
        elif (method == 'get'):
            # get 请求
            print("get 请求")
            if (type != 'json'):
                try:
                    response = requests.get(url, params=data, headers=header)
                    print("get方法获取reponse:" +
                          response.text +
                          "status code:" +
                          str(response.status_code))
                    if(assertText==''):
                        if(response.status_code==200):
                            message="OK"
                        else:
                            message='Fail'
                    else:
                        if(assertText in response.text):
                            message="OK"
                        else:
                            message="Fail"
                except requests.exceptions.MissingSchema:
                    message = "Fail"
                    print("Fail:URL输入错误,No schema supplied.")
                except json.decoder.JSONDecodeError:
                    message = "Fail"
                    print("Fail:hearder或data非json格式")
                except requests.exceptions.ConnectionError:
                    message = "Fail"
                    print("Fail:Fail to establish a new connection.")
            else:
                try:
                    data = json.dumps(data)
                    print(data)
                    response = requests.get(url, params=data, headers=header)
                    print("get方法获取返回值:" +
                          response.text +
                          "statu code:" +
                          str(response.status_code))
                    if (assertText == ''):
                        if (response.status_code == 200):
                            message = "OK"
                        else:
                            message = 'Fail'
                    else:
                        if (assertText in response.text):
                            message = "OK"
                        else:
                            message = "Fail"
                except:
                    message = "Fail"
                    print("Fail:请求失败")
            # return HttpResponse(response)
        else:
            message="Fail:请求方法错误"
            print(message)
        self.assertEqual(message,'OK'),"测试失败"

def runTaskTestcase():
    filename = REPORT_PATH+'/taskResult_.xml'
    print(filename)
    with open(filename, 'w',encoding='utf-8') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output), failfast=False, buffer=False, catchbreak=False)

if __name__=='__main__':
    # print("cmmd parameter:"+str(sys.argv[1]))
    # files=get_file()
    # print(files)
    runTaskTestcase()