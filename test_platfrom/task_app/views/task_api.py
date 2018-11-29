# Create your views here.
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from ..models import Task
from project_app.models.project_models import Project
from project_app.models.module_models import Module
import json
from test_platfrom.common import response_failed,response_succeess
from interface_app.models import Case
from task_app.models import Task
from django.db.models import Q
# Create your views here.
#
#获取用例列表
def selectAjax(request):
    proId = request.GET['para']
    modeList = {}
    # select modules
    mods = Module.objects.filter(project__id=proId)
    for mod in mods:
        modeList[mod.id] = mod.name
    results = json.dumps(modeList)
    print(results)
    response_succeess(results)
# Create your views here.
