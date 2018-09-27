from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
# Create your views here.
#代码处理逻辑
def index(request):
    return render(request,"index.html")
#handle login request

@login_required
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
                context = {"content": "Login successfully"}
                return render(request, "successful.html", context)
                #check userame or password is null
            else:
                context={"content": "username or password is not invalid"}
                return render(request,"fail.html",context)

