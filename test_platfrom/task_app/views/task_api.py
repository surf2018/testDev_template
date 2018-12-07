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
        casename=Case.objects.get(id=case).name
        proname=Case.objects.get(id=case).project.name
        modname=Case.objects.get(id=case).model.name
        caseNames.append({'caseid':case,'casename':casename,'proname':proname,'modname':modname})
    print(caseNames)
    data={"taskname":taskname,"taskDesp":taskDesp,"cases":caseNames}
    return response_succeess(data)

def getZtreeList(request):
    zNodesArray=[]
    #获取所有的case
    cases=Case.objects.all()
    for case in cases:
        caseid=case.id
        casename=case.name
        mid=case.model.id
        nodeList = {'id': caseid, 'pId': mid, 'name': casename}
        zNodesArray.append(nodeList)
    # 获取所有的model追加到zNodesArray
    models = Module.objects.all()
    for model in models:
        modid = model.id
        modname = model.name
        proid = model.project.id
        nodeList = {'id': modid, 'pId': proid, 'name': modname}
        zNodesArray.append(nodeList)
    # 获取所有的project，追加到zNodeArray
    pros = Project.objects.all()
    for pro in pros:
        proid = pro.id
        proname = pro.name
        nodeList = {'id': proid, 'pId': '0', 'name': proname}
        zNodesArray.append(nodeList)
    # 勾选已选的case
    taskid = request.POST['taskid']
    task = Task.objects.get(id=taskid)
    cases = task.cases.strip('[]').replace("'", "").split(',')
    print(zNodesArray)
    return HttpResponse(json.dumps(zNodesArray))
# Create your views here.