from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
#代码处理逻辑
def index(request):
    return render(request,"index.html")
#handle login request



# @login_required
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
                login(request,user)
                context = {"username": name}
                return render(request, "broadcast.html", context)
                #check userame or password is null
            else:
                context={"error": "username or password is not invalid"}
                return render(request,"index.html",context)
def logout_action(request):
    logout(request)
    return render(request,"index.html")


