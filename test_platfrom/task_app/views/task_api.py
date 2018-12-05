# Create your views here.
# from django.shortcuts import render
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect, HttpResponse
# from ..models import Task
# from project_app.models.project_models import Project
from project_app.models.module_models import Module
import json
from test_platfrom.common import response_failed, response_succeess
from interface_app.models import Case
from django.contrib.auth.models import User
from task_app.models import Task
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
# # 编辑用例
# def editTask(request):

# Create your views here.