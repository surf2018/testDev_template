from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
#代码处理逻辑
def index(request):
    return render(request,"index.html")
#handle login request


def login_action(request):
    if(request.method=="POST"):
        print("request post:"+str(request.POST))
        name=request.POST['username']
        passwd=request.POST["password"]
        if(name=="" or passwd==""):
            error = {'error': "name or password should not be empty!"}
            return render(request, "index.html", error)
        else:
            user=authenticate(username=name,password=passwd)
            if(user is not None):
                login(request,user)#记录用户登陆状态
                request.session['username']=name
                return HttpResponseRedirect('/broadcast/')
                # response=HttpResponseRedirect('/broadcast/')
                # response.set_cookie('username',name,3600)
                # return response
                #check userame or password is null
            else:
                context={"error": "username or password is not invalid"}
                return render(request,"index.html",context)
@login_required
def broadcast(request):
    # username=request.COOKIES.get('username','')
    username=request.session.get('username','')
    context={'username':username}
    return render(request,'broadcast.html',context)
def logout_action(request):
    logout(request)
    return HttpResponseRedirect("/login")


