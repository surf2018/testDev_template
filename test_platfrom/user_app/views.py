from django.shortcuts import render

# Create your views here.
#代码处理逻辑
def index(request):
    return render(request,"index.html")
#handle login request
def login_action(request):
    if(request.method=="GET"):
        name=request.GET.get("username")
        passwd=request.GET.get("password")
        #check userame or password is null
        if(name=="" or passwd==""):
            error={'error':"name or password should not be empty!"}
            return  render(request,"index.html",error)