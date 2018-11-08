from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from ..models import Case
from project_app.models.project_models import Project
from project_app.models.module_models import Module
from django.contrib.auth.models import User

from ..case_forms import CaseForm
# Create your views here.
#
@login_required
def caselist(request):
    username = request.session.get('username', '')
    type = request.GET['type']
    if (type == '' or type == 'caselist'):
        case=Case.objects.all()
        # 分页
        paginator = Paginator(case, 10)
        page = request.GET.get('page', 1)
        curpage = int(page)
        try:
            print(page)
            case = paginator.page(curpage)
        except PageNotAnInteger:
            case = paginator.page(1)
        except EmptyPage:
            case = paginator.page(paginator.num_pages)
        context = {'username': username,'type': type, 'cases':case}
        return render(request, 'case/testcase.html', context)
    if(type == 'create'):
        pros=Project.objects.all()
        mods=Module.objects.all()
        context= {'username': username,'type': type,'pros':pros,'mods':mods}
        return render(request, 'case/add_case.html', context)

    elif(type=='debug'):
        context = {'username': username, 'type': type}
        return render(request,'case/api_debug.html',context)
@csrf_exempt
def debug_ajax(request):
    if(request.method=='POST'):
        url=request.POST['url']
        method=request.POST['method']
        type=request.POST['type']
        header=json.loads(request.POST['header'])
        data=request.POST['parameter']
        # data=json.loads(data)
        data=eval(data)
        if(method=='post'):
            #post 请求
            if(type!='json'):
                if ('file' in data.keys()):
                    response = requests.post(url, files=data)
                    print(response)
                else:
                    response=requests.post(url,data=data,headers=header)
                    print("post"+response.text+"status code:"+str(response.status_code))
            else:
                print("post 请求json")
                data=json.dumps(data)
                response=requests.post(url,data=data,headers=header)
                print("post" + response.text + "status code:" + str(response.status_code))
        elif(method=='get'):
            #get 请求
            print("get 请求")
            if(type!='json'):
                response=requests.get(url,params=data,headers=header)
                print("get:"+response.text+"status code:"+str(response.status_code))
            else:
                data = json.dumps(data)
                response=requests.get(url,params=data,headers=header)
                print("get:"+response.text+"statu code:"+str(response.status_code))
        return HttpResponse(response)
    else:
        username = request.session.get('username', '')
        context = {'username': username, 'type': 'debug'}
        return render(requests,'case/api_debug.html',context)

def saveDate(request):
    username=request.POST['username']
    userid=User.objects.get(username=username).id
    proid=request.POST['proid']
    modid=request.POST['modid']
    name=request.POST['name']
    url=request.POST['url']
    method=request.POST['method']
    type=request.POST['type']
    header=request.POST['header']
    parameter=request.POST['parameter']
    status=request.POST['status']
    print(status)
    case=Case(name=name,url=url,method=method,type=type,header=header,data=parameter,status=status,create_user_id=userid,model_id=modid,project_id=proid)
    case.save()
    return HttpResponse('save ok')
def selectAjax(request):
    proId=request.GET['para']
    modeList={}
    #select modules
    mods=Module.objects.filter(project__id=proId)
    for mod in mods:
        modeList[mod.id]=mod.name
    results=json.dumps(modeList)
    print(results)
    return HttpResponse(results,content_type='application/json')
def debugCase(request,caseid):
    cases=Case.objects.get(id=caseid)
    proname=cases.project
    modname=cases.model
    username = request.session.get('username', '')
    context = {'username': username, 'case':cases,'pro':proname,'mod':modname}
    return render(request, 'case/api_debug.html', context)

# Create your views here.