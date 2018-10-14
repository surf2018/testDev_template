from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
#代码处理逻辑
def index(request):
    return render(request,"user/index.html")
#handle login request
def login_action(request):
    if(request.method=="POST"):
        print("request post:"+str(request.POST))
        name=request.POST['username']
        passwd=request.POST["password"]
        if(name=="" or passwd==""):
            error = {'error': "name or password should not be empty!"}
            return render(request, "user/index.html", error)
        else:
            user=authenticate(username=name,password=passwd)
            if(user is not None):
                login(request,user)#记录用户登陆状态
                request.session['username']=name
                # context={'type':'list'}
                # return render(request,'project/broadcast.html',context)
                return HttpResponseRedirect('/project/dashboard?type=plist')
                # response.set_cookie('username',name,3600)
                # return response
                #check userame or password is null
            else:
                context={"error": "username or password is not invalid"}
                return render(request,"user/index.html",context)

def logout_action(request):
    logout(request)
    return HttpResponseRedirect("/user")