
import request
import json
from ddt import ddt,data,unpack
import unittest
import csv
import requests
from test_platfrom.common import response_failed,response_succeess
#测试数据
def get_data(file_name):
    # print("file_name"+str(file_name))
    # create an empty list to store rows
    rows = []
    # open the CSV file
    data_file = open(file_name, "r")
    # create a CSV Reader from CSV file
    reader = csv.reader(data_file)
    # skip the headers
    next(reader, None)
    # add rows from reader to list
    for row in reader:
        rows.append(row)
    print(rows)
    return rows
@ddt
class ccaSystem(unittest.TestCase):
    def setUp(self):
        print("running test task")

    @data(*get_data("test_data.csv"))
    @unpack
    def test_run(self,url,method,type,header,data,assertText):
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
                            message="Ok"
                except requests.exceptions.ConnectionError:
                    message = "Failed to establish a new connection."
                    print(message)
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
                    message = "URL输入错误;No schema supplied."
                    return response_failed(message)
                except json.decoder.JSONDecodeError:
                    message = "hearder或data非json格式"
                    return response_failed(message)
                except requests.exceptions.ConnectionError:
                    message = " Failed to establish a new connection."
            else:
                data = json.dumps(data)
                try:
                    response = requests.get(url, params=data, headers=header)
                    print("get方法获取返回值:" +
                          response.text +
                          "statu code:" +
                          str(response.status_code))
                except:
                    message = "请求失败"
            try:
                data = json.loads(response.text)
                print("data")
            except json.decoder.JSONDecodeError:
                message = "请求失败"
                print(message)
            # return HttpResponse(response)
        else:
            message="请求方法错误"
            print(message)
        self.assertEqual(message,"OK"),"test fail"