# Create your views here.
# from django.shortcuts import render
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect, HttpResponse
# from ..models import Task
# from project_app.models.project_models import Project
from project_app.models.module_models import Module,Project
import json
from test_platfroms.common import response_failed, response_succeess
from interface_app.models import Case
from django.contrib.auth.models import User
from task_app.models import Task
from django.http import HttpResponse
from task_app.extend.task_thread import TaskThread

import os
import xml.etree.cElementTree as ET

from django.db.models import Q


# Create your views here.
#
# 获取用例列表
def selectAjax(request):
    proId = request.GET['ppara']
    modId = request.GET['mpara']
    modeList = {}
    caseList = {}
    # 查询所属项目id的所有模块
    mods = Module.objects.filter(project__id=proId)
    # 查询属于项目的所有case
    if (modId == "-1"):
        cases = Case.objects.filter(project__id=proId)
    else:
        cases = Case.objects.filter(project__id=proId, model__id=modId)
    print(cases)
    for mod in mods:
        modeList[mod.id] = mod.name
    for case in cases:
        caseList[case.id] = case.name
    datas = {"modList": modeList, "caseList": caseList, "modId": modId}
    results = json.dumps(datas)
    print(results)
    return response_succeess(results)

#保存新数据
def save(request):
    name = request.session.get('username', '')
    userId = User.objects.get(username=name).id
    taskName = request.POST['taskName']
    taskDesp = request.POST['taskDesp']
    taskResult = request.POST["taskResult"]
    taskStat = request.POST['taskStat']
    caseList = request.POST.getlist('caseList')
    print("caselist:" + str(caseList))

    # check taskname是否存在
    task = Task.objects.filter(name=taskName)
    if (task):
        print("task" + taskName + "has been exist")
        return response_failed("task:" + taskName + " 已经存在,保存失败")
    else:
        task = Task(
            name=taskName,
            description=taskDesp,
            status=taskStat,
            result=taskResult,
            create_user_id=userId,
            cases=caseList)
        task.save()
        return response_succeess(data="保存成功")
# 根据ajax传的taskid来查询caseid
def queryTask(request):
    taskid=request.POST['taskid']
    task=Task.objects.get(id=taskid)
    taskname=task.name
    taskDesp=task.description
    cases=task.cases.strip('[]').replace("'","").split(',')
    caseNames=[]
    for case in cases:
        case=case.strip()
        casename=Case.objects.get(id=int(case)).name
        proname=Case.objects.get(id=int(case)).project.name
        modname=Case.objects.get(id=int(case)).model.name
        caseNames.append({'caseid':case,'casename':casename,'proname':proname,'modname':modname})
    # print(caseNames)
    data={"taskname":taskname,"taskDesp":taskDesp,"cases":caseNames}
    return response_succeess(data)

def getZtreeList(request):
    zNodesArray=[]
    #获取已经有的testcase
    taskid=request.POST['taskid']
    task = Task.objects.get(id=taskid)
    TaskCases = task.cases.strip('[]').replace("'","").replace(" ","").split(',')
    print("TaskCases"+str(TaskCases))
    #获取选中的对应的model和project
    TaskcaseInfo=[]
    info={}
    for caseid in TaskCases:
        modid=Case.objects.get(id=int(caseid)).model.id
        proid=Case.objects.get(id=int(caseid)).project.id
        info={'caseid':caseid,'modid':modid,'proid':proid}
        TaskcaseInfo.append(info)
    print("选中task信息："+str(TaskcaseInfo))
    # 获取所有的project，追加到zNodeArray
    pros = Project.objects.all()
    for pro in pros:
        proid = pro.id
        proname = pro.name
        nodeList = {'id': proid, 'name': proname, 'open': 'true'}
        #查询pro下的子节点模块的信息
        mods=Module.objects.filter(project__id=proid)
        zNodesArray.append(nodeList)
        for mod in mods:
            lmodid=mod.id*200
            modname=mod.name
            nodeList_2 = {'id': lmodid, 'name': modname, 'pId': proid, 'open':'true'}
            #获取mode下的case信息，如果case在已选择的case里面那么勾选
            cases=Case.objects.filter(model__id=mod.id)
            zNodesArray.append(nodeList_2)
            for case in cases:
                caseid=str(case.id)
                lcaseid=case.id*40000
                casename=case.name
                if caseid in TaskCases:
                    nodeList = {'id': lcaseid, 'pId': lmodid, 'name': casename,'checked':'true'}
                else:
                    nodeList = {'id': lcaseid, 'pId': lmodid, 'name': casename}
                zNodesArray.append(nodeList)
    print(zNodesArray)
    return HttpResponse(json.dumps(zNodesArray))

#更新数数据
def update(request):
    name = request.session.get('username', '')
    userId = User.objects.get(username=name).id
    taskid=request.POST['taskid']
    taskName = request.POST['taskName']
    taskDesp = request.POST['taskDesp']
    # taskResult = request.POST["taskResult"]
    # taskStat = request.POST['taskStat']
    caseList = request.POST.getlist('caseList')
    print("caselist:" + str(caseList))
    # check taskname是否存在
    task = Task.objects.filter(name=taskName).exclude(id=taskid)
    if (task):
        print("task" + taskName + "has been exist")
        return response_failed("task:" + taskName + " 已经存在,保存失败")
    else:
        task = Task.objects.filter(id=taskid).update(
            name=taskName,
            description=taskDesp,
            # status=taskStat,
            # result=taskResult,
            create_user_id=userId,
            cases=caseList)
        return response_succeess(data="更新成功")
#create take and edit task页面运行任务
def runTask(request):
    #判断有没有其他任务在执行
    flag=0
    tasks=Task.objects.all()
    for task in tasks:
        if(task.status=='1'):
            flag=1
            break
    if(flag==1):
        return response_failed("有任务在执行，请稍后执行")
    else:
        #将获取到的testcase的列表写入json文件
        taskid = request.POST['taskid']
        print("receive taskid:" + str(taskid))
        #更新taske状态值
        Task.objects.filter(id=taskid).update(status='1',result='-1')
        #运行任务
        th=TaskThread(taskid)
        th.new_run()
        #查看数据库的值
        task=Task.objects.get(id=taskid)
        re=task.result
        if(re=='0'):
            return response_succeess("测试NG")
        else:
            return response_succeess('测试OK')
def getStatus(request):
    taskid=request.POST['taskid']
    task=Task.objects.get(id=int(taskid))
    task_result=task.result
    if(task_result=='0'):
        message="测试NG"
    else:
        message="测试OK"
    return response_succeess(message)
    #返回结果到ajax
#接续介乎
# Create your views here.