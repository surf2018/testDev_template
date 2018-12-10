# Create your views here.
# from django.shortcuts import render
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect, HttpResponse
# from ..models import Task
# from project_app.models.project_models import Project
from project_app.models.module_models import Module,Project
import json
from test_platfrom.common import response_failed, response_succeess
from interface_app.models import Case
from django.contrib.auth.models import User
from task_app.models import Task
from django.http import HttpResponse
from task_app.apps import TASK_PATH,TASK_RUN_PATH
import os

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
        casename=Case.objects.get(id=int(case)).name
        proname=Case.objects.get(id=int(case)).project.name
        modname=Case.objects.get(id=int(case)).model.name
        caseNames.append({'caseid':case,'casename':casename,'proname':proname,'modname':modname})
    print(caseNames)
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
    taskResult = request.POST["taskResult"]
    taskStat = request.POST['taskStat']
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
            status=taskStat,
            result=taskResult,
            create_user_id=userId,
            cases=caseList)
        return response_succeess(data="更新成功")
#运行任务
def runTask(request):
    #将获取到的testcase的列表写入json文件
    caseList=request.POST.getlist('caseList')
    taskid=request.POST['taskid']
    print("receive testcase list"+str(caseList))
    case_dict={}
    for case in caseList:
        caseInfo=Case.objects.get(id=int(case))
        case_url=caseInfo.url
        case_method=caseInfo.method
        case_type=caseInfo.type
        case_header=caseInfo.header
        case_data=caseInfo.data
        case_assert=caseInfo.response_assert
        case_dict[case]={'url':case_url,'method':case_method,'type':case_type,'header':case_header,'data':case_data,'assertText':case_assert}
    print("runTask_json:")
    print(case_dict)
    #写入json文件
    taskJsonPath=TASK_PATH+"/task_"+taskid+".json"
    with open(taskJsonPath, "w") as f:
        json.dump(case_dict, f)
    print("加载入文件完成...")
    #调用程序执行脚本
    print("运行:"+TASK_RUN_PATH+"用例")
    command="python " + TASK_RUN_PATH+" "+taskid
    print("命令:"+command)
    os.system("python " + TASK_RUN_PATH+" "+taskid)
    #解析xml文件
    result=1
    if(result==1):
        return response_succeess(data="运行成功")
    else:
        return response_failed("运行失败")

    # for case
# Create your views here.