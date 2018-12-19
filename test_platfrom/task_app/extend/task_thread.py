import threading
from interface_app.models import Case
from task_app.models import TaskResult
from task_app.models import Task
from task_app.apps import TASK_PATH, TASK_RUN_PATH, REPORT_PATH
import json
import os
import xml.etree.cElementTree as ET


class TaskThread():
    def __init__(self, taskid):
        self.taskid = int(taskid)

    def readResult(self):
        # 读取文件所有内容
        resultPath = REPORT_PATH + "/taskResult.xml"
        f = open(resultPath, 'r')
        content = f.read()
        f.close()
        return content

    def parseResultXml(self):
        # 解析xml文件
        resultList = {}
        # 读取文件所有内容：
        content = self.readResult()
        resultPath = REPORT_PATH + "/taskResult.xml"
        tree = ET.ElementTree(file=resultPath)
        root = tree.getroot()
        print(root.tag)
        if (root.tag == "testsuite"):
            print(root.attrib)
            resultList['errors'] = root.attrib['errors']
            resultList['failures'] = root.attrib['failures']
            resultList['name'] = root.attrib['name']
            if ('skipped' in root.attrib):
                resultList['skipped'] = root.attrib['skipped']
            else:
                resultList['skipped'] = 0
            resultList['tests'] = root.attrib['tests']
            resultList['time'] = root.attrib['time']
            resultList['content'] = content
        print("结果分析：" + str(resultList))
        return resultList

    def wirtToDB(self, resultList):
        try:
            taskResult = TaskResult(
                name=resultList['name'],
                error=resultList['errors'],
                failures=resultList['failures'],
                skipped=resultList['skipped'],
                tests=resultList['tests'],
                run_time=resultList['time'],
                result=resultList['content'],
                task_id=self.taskid)
            taskResult.save()
            print("已经保存到数据库")
            result = 1
        except Exception as e:
            print(e)
            result = 0
        return result

    def runing_task(self):
        # 查询taskid
        result = 0
        # 查询数据库
        caseListStr = Task.objects.get(id=self.taskid).cases
        caseList = caseListStr.strip('[]').replace("'", "").split(",")
        print(caseList)
        case_dict = {}
        for case in caseList:
            case = case.strip()
            caseInfo = Case.objects.get(id=int(case))
            case_url = caseInfo.url
            case_method = caseInfo.method
            case_type = caseInfo.type
            case_header = caseInfo.header
            case_data = caseInfo.data
            case_assert = caseInfo.response_assert
            case_dict[case] = {'url': case_url, 'method': case_method, 'type': case_type, 'header': case_header,
                               'data': case_data, 'assertText': case_assert}
        # print("runTask_json:")
        print(case_dict)
        # 写入json文件
        taskJsonPath = TASK_PATH + "/task.json"
        with open(taskJsonPath, "w") as f:
            json.dump(case_dict, f)
        # print("加载入文件完成...")
        # 调用程序执行脚本
        # print("运行:" + TASK_RUN_PATH + "用例")
        command = "python " + TASK_RUN_PATH
        # print("命令:" + command)
        os.system("python " + TASK_RUN_PATH)

    def run(self):
        threads = []
        t = threading.Thread(target=self.runing_task)
        threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        # print("任务执行完毕，分析结果")
        resultList = self.parseResultXml()
        # 写入数据库
        if (len(resultList) > 0):
            # print("写数据库")
            self.wirtToDB(resultList)
        else:
            print("")
            # print("结果文件没有生成")
        # 更改task的数据的状态
        if (resultList['failures'] == '0' and resultList['errors'] == '0' and int(resultList['tests']) > 0):
            Task.objects.filter(id=self.taskid).update(status='2', result='1')
            message = "任务成功"
        else:
            Task.objects.filter(id=self.taskid).update(status='2', result='0')
            message = "任务失败"
        print(message)
        return message

    def new_run(self):
        threads = []
        t = threading.Thread(target=self.run)
        threads.append(t)
        for i in threads:
            i.start()
