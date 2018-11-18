from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from ..models import Case
from project_app.models.project_models import Project
from project_app.models.module_models import Module
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers
from ..case_forms import CaseForm


# Create your views here.
#
@login_required
def caselist(request):
    username = request.session.get('username', '')
    type = request.GET['type']
    if (type == '' or type == 'caselist'):
        case = Case.objects.all()
        # 分页
        paginator = Paginator(case, 5)
        page = request.GET.get('page', 1)
        curpage = int(page)
        try:
            print(page)
            case = paginator.page(curpage)
        except PageNotAnInteger:
            case = paginator.page(1)
        except EmptyPage:
            case = paginator.page(paginator.num_pages)
        context = {'username': username, 'type': type, 'cases': case}
        return render(request, 'case/testcase.html', context)
    if (type == 'create'):
        pros = Project.objects.all()
        mods = Module.objects.all()
        context = {
            'username': username,
            'type': type,
            'pros': pros,
            'mods': mods}
        return render(request, 'case/add_case.html', context)

    elif (type == 'debug'):
        context = {'username': username, 'type': type}
        return render(request, 'case/api_debug.html', context)


# 点击debug的处理
@csrf_exempt
def debug_ajax(request):
    if (request.method == 'POST'):
        url = request.POST['url']
        method = request.POST['method']
        type = request.POST['type']
        header = json.loads(request.POST['header'])
        data = request.POST['parameter']
        print(data)
        # 转换为json格式
        data = json.loads(data, strict=False)
        print(data)
        # data=eval(data)
        if (method == 'post'):
            # post 请求
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
                data = json.dumps(data)
                response = requests.post(url, data=data, headers=header)
                print("post" +
                      response.text +
                      "status code:" +
                      str(response.status_code))
        elif (method == 'get'):
            # get 请求
            print("get 请求")
            if (type != 'json'):
                response = requests.get(url, params=data, headers=header)
                print("get:" +
                      response.text +
                      "status code:" +
                      str(response.status_code))
            else:
                data = json.dumps(data)
                response = requests.get(url, params=data, headers=header)
                print("get:" +
                      response.text +
                      "statu code:" +
                      str(response.status_code))
        return HttpResponse(response)
    else:
        username = request.session.get('username', '')
        context = {'username': username, 'type': 'debug'}
        return render(requests, 'case/api_debug.html', context)


# 保存新建数据
def saveDate(request):
    username = request.POST['username']
    userid = User.objects.get(username=username).id
    proid = request.POST['proid']
    modid = request.POST['modid']
    name = request.POST['name']
    url = request.POST['url']
    method = request.POST['method']
    type = request.POST['type']
    header = request.POST['header']
    parameter = request.POST['parameter']
    status = request.POST['status'].title()
    print(status)
    response_assert = request.POST['assert']
    case = Case(
        name=name,
        url=url,
        method=method,
        type=type,
        header=header,
        data=parameter,
        status=status,
        response_assert=response_assert,
        create_user_id=userid,
        model_id=modid,
        project_id=proid)
    case.save()
    return HttpResponse('save ok')


# select联动接口
def selectAjax(request):
    proId = request.GET['para']
    modeList = {}
    # select modules
    mods = Module.objects.filter(project__id=proId)
    for mod in mods:
        modeList[mod.id] = mod.name
    results = json.dumps(modeList)
    print(results)
    return HttpResponse(results, content_type='application/json')


def debugCase(request, caseid):
    username = request.session.get('username', '')
    context = {'username': username, 'type': 'debug', 'caseid': caseid}
    return render(request, 'case/api_debug.html', context)


# editcase and update case
def updateDate(request):
    username = request.POST['username']
    userid = User.objects.get(username=username).id
    caseid = request.POST['caseid']
    proid = request.POST['proid']
    modid = request.POST['modid']
    name = request.POST['name']
    url = request.POST['url']
    method = request.POST['method']
    type = request.POST['type']
    header = request.POST['header']
    parameter = request.POST['parameter']
    status = request.POST['status']
    response_assert = request.POST['assert']
    print(status)
    Case.objects.filter(
        id=caseid).update(
        name=name,
        url=url,
        method=method,
        type=type,
        header=header,
        data=parameter,
        status=status.title(),
        response_assert=response_assert,
        create_user_id=userid,
        model_id=modid,
        project_id=proid)
    return HttpResponse('Update ok')


def delCase(request, caseid):
    # 删除数据库
    Case.objects.filter(id=caseid).delete()
    return HttpResponseRedirect("/interface/case_manager/?type=caselist")


# search case (name,url,method,project name,method name )
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


# 跳转到api_debug.html
def returnApiDebug(request):
    username = request.session.get('username', '')
    context = {
        'username': username,
        'type': 'debug'}
    return render(request, 'case/api_debug.html', context)


def queryCaseAjax(request):
    # 处理editCaseAjax
    caseid = request.POST['caseid']
    cases = Case.objects.get(id=caseid)
    pros = serializers.serialize("json", Project.objects.all())
    mods = serializers.serialize("json", Module.objects.all())
    sscases = serializers.serialize("json", Case.objects.filter(id=caseid))
    proname = cases.project.name
    # print(proname)
    modname = cases.model.name
    # print(modname)
    # username = request.session.get('username', '')
    context = {
        # 'username': username,
        'cases': sscases,
        'proname': proname,
        'modname': modname,
        'pros': pros,
        'mods': mods,
        'type': 'debug'}
    # print(context)
    results = json.dumps(context)
    print(results)
    return HttpResponse(results, content_type='application/json')


def assertResult(request):
    aResult = request.POST['assertResult']
    rResult = request.POST['returnResult']
    if (aResult in rResult):
        result = "验证成功"
    else:
        result = "验证失败"
    return HttpResponse(result)
# Create your views here.
