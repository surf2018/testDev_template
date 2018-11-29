# Create your views here.
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from ..models import Task
from project_app.models.project_models import Project
from project_app.models.module_models import Module
from interface_app.models import Case
from task_app.models import Task
from django.db.models import Q
# Create your views here.
#
#获取用例列表
@login_required
def tasklist(request):
    username = request.session.get('username', '')
    type = request.GET['type']
    if (type == '' or type == 'tasklist'):
        tasks = Task.objects.all()
        # 分页
        paginator = Paginator(tasks, 5)
        page = request.GET.get('page', 1)
        curpage = int(page)
        try:
            print(page)
            tasks = paginator.page(curpage)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)
        context = {'username': username, 'type': type, 'tasks': tasks}
        return render(request, 'task/task.html', context)
    #创建测试用例
    if (type == 'create'):
        pros=Project.objects.all()
        context = {
            'username': username,
            'type': type,
            'pros':pros
        }
        return render(request, 'task/add_task.html', context)
# 编辑用例
def debugCase(request, caseid):
    username = request.session.get('username', '')
    context = {'username': username, 'type': 'debug', 'caseid': caseid}
    return render(request, 'case/api_debug.html', context)

#删除用例
def delCase(request, caseid):
    # 删除数据库
    Case.objects.filter(id=caseid).delete()
    return HttpResponseRedirect("/interface/case_manager/?type=caselist")


# 搜索 case (用例名称搜索，用例url搜索,用例method搜索,用例所属项目搜索，用例所属模块搜索)
def searchCase(request):
    query_text = request.GET['search']
    if (query_text == ""):
        caseInfo = Case.objects.all()
        # contex={"error":"请输入搜索字符"}
        return HttpResponseRedirect(
            "/interface/case_manager/?type=caselist", caseInfo)
    else:
        username = request.session.get('username', '')
        # search case通过name,url,method,status,projectName,modelName
        caseInfo = Case.objects.filter(
            Q(
                name__icontains=query_text) | Q(
                url__icontains=query_text) | Q(
                method__icontains=query_text) | Q(
                status__icontains=query_text) | Q(
                project__name__icontains=query_text) | Q(
                model__name__icontains=query_text))
        # 分页，每5个分页
        paginator = Paginator(caseInfo, 5)
        page = request.GET.get("page", 1)
        curpage = int(page)
        try:
            caseInfo = paginator.page(curpage)
        except PageNotAnInteger:
            caseInfo = paginator.page(1)
        except EmptyPage:
            caseInfo = paginator.page(paginator.num_pages)
        context = {
            'cases': caseInfo,
            'username': username,
            'type': 'caselist',
            'search': query_text}
        return render(request, "case/testcase.html", context)
# Create your views here.
