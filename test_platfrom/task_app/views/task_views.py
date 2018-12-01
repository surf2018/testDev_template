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
        print(context)
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

# # 编辑任务
# def debugCase(request, caseid):
#     username = request.session.get('username', '')
#     context = {'username': username, 'type': 'debug', 'caseid': caseid}
#     return render(request, 'case/api_debug.html', context)

# #删除任务
# def delTask(request, taskid):
#     # 从数据库里删除任务
#     Task.objects.filter(id=taskid).delete()
#     return HttpResponseRedirect("/task/task_manager/?type=caselist")


# # 搜索任务
# def searchTask(request):
#     query_text = request.GET['search']
#     if (query_text == ""):
#         taskInfo = Task.objects.all()
#         # contex={"error":"请输入搜索字符"}
#         return HttpResponseRedirect(
#             "/task/task_manager/?type=tasklist", taskInfo)
#     else:
#         username = request.session.get('username', '')
#         # search case通过name,url,method,status,projectName,modelName
#         taskInfo = Task.objects.filter(
#             Q(name__icontains=query_text) | Q(description__icontains=query_text))
#         # 分页，每5个分页
#         paginator = Paginator(taskInfo, 5)
#         page = request.GET.get("page", 1)
#         curpage = int(page)
#         try:
#             taskInfo = paginator.page(curpage)
#         except PageNotAnInteger:
#             taskInfo = paginator.page(1)
#         except EmptyPage:
#             taskInfo = paginator.page(paginator.num_pages)
#         context = {
#             'cases': taskInfo,
#             'username': username,
#             'type': 'tasklist',
#             'search': query_text}
#         return render(request, "task/task.html", context)
# Create your views here.
