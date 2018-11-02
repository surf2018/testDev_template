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
        header=request.POST['header']
        data=request.POST['parameter']
        data=json.loads(data)
        if(method=='post'):
            #post 请求
            if(type!='json'):
                response=requests.post(url,data=data,headers=header)
                print(response.text)
            # else:
                #post 请求json

        elif(method=='get'):
            #get 请求
            if(type!='json'):
                response=requests.get(url,params=data)
            # else:

        return HttpResponse(response)
    else:
        username = request.session.get('username', '')
        context = {'username': username, 'type': 'debug'}
        return render(requests,'case/api_debug.html',context)




# Create your views here.
