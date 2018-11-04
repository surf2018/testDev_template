from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
# Create your views here.
#
@login_required
def caselist(request):
    username = request.session.get('username', '')
    type = request.GET['type']
    if (type == '' or type == 'caselist'):
        context = {'username': username,'type': type}
        return render(request, 'case/testcase.html', context)
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




# Create your views here.
