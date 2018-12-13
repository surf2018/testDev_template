from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from test_platfroms.common import response_failed,response_succeess
from ..models import Case
from project_app.models.project_models import Project
from project_app.models.module_models import Module
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers
# Create your views here.

# 对send(请求)的处理，后台返回值
@csrf_exempt
def debug_ajax(request):
    if (request.method == 'POST'):
        url = request.POST['url']
        method = request.POST['method']
        type = request.POST['type']
        try:
            header = json.loads(request.POST['header'])
            data = request.POST['parameter']
            print(data)
            # 转换为json格式
            # data=eval(data)
            data = json.loads(data, strict=False)
            print(data)
        except json.decoder.JSONDecodeError:
            message = "hearder或data非json格式"
            return response_failed(message)
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
                try:
                    data = json.dumps(data)
                    response = requests.post(url, data=data, headers=header)
                    print("post" +
                          response.text +
                          "status code:" +
                          str(response.status_code))
                except requests.exceptions.ConnectionError:
                    message = "Failed to establish a new connection."
                    return response_failed(message)
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
                except requests.exceptions.MissingSchema:
                    message="URL输入错误;No schema supplied."
                    return response_failed(message)
                except json.decoder.JSONDecodeError:
                    message="hearder或data非json格式"
                    return response_failed(message)
                except requests.exceptions.ConnectionError:
                    message=" Failed to establish a new connection."
                    return response_failed(message)
            else:
                data = json.dumps(data)
                try:
                    response = requests.get(url, params=data, headers=header)
                    print("get方法获取返回值:" +
                          response.text +
                          "statu code:" +
                          str(response.status_code))
                except:
                    message="请求失败"
                    return response_failed(message)
        try:
            data = json.loads(response.text)
            return response_succeess(data=data)
        except json.decoder.JSONDecodeError:
            message = "请求失败"
            return response_failed(message)
        # return HttpResponse(response)
    else:
        return response_failed("请求方法错误")
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
    #check casename和url是否存在
    case=Case.objects.filter(name=name)
    case2=Case.objects.filter(url=url)
    if(case):
        print("case"+name+"has been exist")
        return response_failed("case:"+name+" 已经存在")
    elif(case2):
        print("url:"+url+" has been exist")
        return response_failed("url:"+url+"已经存在")
    else:
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
        return response_succeess(data="保存成功")
    # return HttpResponse('save ok')
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
# 编辑用例并更新用例
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
    #check casename and url是否已经存在
    case = Case.objects.filter(name=name).exclude(id=caseid)
    case2 = Case.objects.filter(url=url).exclude(id=caseid)
    if (case):
        print("case" + name + "has been exist")
        return response_failed("case:" + name + " 已经存在")
    elif (case2):
        print("url:" + url + " has been exist")
        return response_failed("url:" + url + "已经存在")
    else:
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
        return response_succeess("更新成功")

# 点击返回,跳转到api_debug.html
def returnApiDebug(request):
    username = request.session.get('username', '')
    context = {
        'username': username,
        'type': 'debug'}
    return render(request, 'case/api_debug.html', context)

#接收前端传来的caseid查询case的信息
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

#验证结果
def assertResult(request):
    aResult = request.POST['assertResult']
    rResult = request.POST['returnResult']
    if (aResult in rResult):
        result = "验证成功"
        return response_succeess(result)
    else:
        result = "验证失败"
        return response_failed(result)

# Create your views here.
