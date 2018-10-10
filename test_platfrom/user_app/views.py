from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from .models import Project,Version
from django.db.models import Q
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
    projects=Project.objects.all()
    #分页
    paginator = Paginator(projects, 10)
    page = request.GET.get('page', 1)
    curpage = int(page)
    try:
        print(page)
        projects=paginator.page(curpage)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    context={'username':username,'projects':projects}
    #query databases dispaly all projects
    return render(request,'broadcast.html',context)

def logout_action(request):
    logout(request)
    return HttpResponseRedirect("/login")

def createProject(request):
    return render(request,"createProject.html")

def createP_action(request):
    if(request.method=='POST'):
        pname=request.POST['name']
        desp=request.POST['description']
        stime=request.POST['starttime']
        endtime=request.POST['endtime']
        status=request.POST['status']
        if(pname=="" or desp=="" or stime==""):
            error={"error":"项目名,项目描述和创建时间不能为空"}
            return render(request,"createProject.html",error)
        else:
            #write to database
            project=Project(name=pname,description=desp,createTime=stime,endTime=endtime,status=status)
            project.save()
            return HttpResponseRedirect("/broadcast")
def createVersion(request):
    pname=request.GET['name']
    context={'projectname':pname}
    return render(request,"createVersion.html",context)

def createV_acton(request):
    #写入数据
    if(request.method=='POST'):
        username=request.session.get("username","")
        projectname=request.GET['name']
        pinfo=Project.objects.get(name=projectname)
        version=request.POST['version']
        desp=request.POST['description']
        starttime=request.POST['starttime']
        release=request.POST['isrelease']
        endtime=request.POST['endtime']
        criticals=request.POST['critical']
        majors=request.POST['major']
        pversion=Version(version=version,description=desp,release=release,project_id=pinfo.id,createtime=starttime,endtime=endtime,Criticalbugs=criticals,Majorbugs=majors)
        pversion.save()
        return HttpResponseRedirect("/queryVersion/?user="+username+"&name="+projectname+"&id="+str(pinfo.id))
def queryVersion(request):
    user=request.session.get('username',"")
    pname=request.GET['name']
    pid=request.GET['id']
    #查询数据库
    verinfo=Version.objects.filter(project_id=pid)
    #分页
    paginator=Paginator(verinfo,10)
    page=request.GET.get('page',1)
    curpage=int(page)
    try:
        verinfo=paginator.page(curpage)
    except PageNotAnInteger:
        verinfo.paginator.page(1)
    except EmptyPage:
        verinfo.paginator.page(paginator.num_pages)
    context={'user':user,'projectname':pname,"projectid":pid,"versions":verinfo}
    return render(request,"queryVersion.html",context)
def editProject(request):
    pname=request.GET['name']
    pid=request.GET['id']
    pro=Project.objects.filter(name=pname,id=pid)
    context={'pid':pid,'projectname':pname,'description':pro[0].description,'starttime':pro[0].createTime,'endtime':pro[0].endTime,'status':pro[0].status}
    print("context:"+str(context))
    return render(request,"editProject.html",context)
def editP_action(request):
    #数据库中更新数据
    id=request.GET['id']
    newname=request.POST['name']
    newdep=request.POST['description']
    newStartTime=request.POST['starttime']
    newendTime=request.POST['endtime']
    newstatus=request.POST['status']
    if(newname!=''and newdep!='' and newStartTime!=''):
        Project.objects.filter(id=id).update(name=newname,description=newdep,createTime=newStartTime,endTime=newendTime,status=newstatus)
        return HttpResponseRedirect("/broadcast")
    else:
        context={'error':'项目名，项目描述，项目开始时间不能为空！'}
        render(request,"editProject.html",context)
def delProject(request):
    # name=request.GET['name']
    id=request.GET['id']
    #删除数据库
    Project.objects.filter(id=id).delete()
    return HttpResponseRedirect("/broadcast")
def editVersion(request):
    vid=request.GET['vid']
    #query数据库
    verInfo=Version.objects.get(id=vid)
    return render(request,"editVersion.html",{'versionInfo':verInfo})
def editV_action(request):
    vid=request.GET['vid']
    newVer=request.POST['versionId']
    newdesp=request.POST['verdesp']
    newstarttime=request.POST['starttime']
    newendtime=request.POST['endtime']
    newcritical=request.POST['critical']
    newmajor=request.POST['major']
    newrelease=request.POST['isrelease']
    if(newVer!=''and newdesp!=''and newstarttime!=''and newendtime!=''and newcritical!=''and newmajor!=''and newrelease!=''):
        Version.objects.filter(id=vid).update(version=newVer,description=newdesp,createtime=newstarttime,endtime=newendtime,Criticalbugs=newcritical,Majorbugs=newmajor,release=newrelease)
        vinfo=Version.objects.get(id=vid)
        pid=vinfo.project_id
        pinfo=Project.objects.get(id=pid)
        pname=pinfo.name
        username=request.session.get("username","")
        return HttpResponseRedirect("/queryVersion/?user="+username+"&name="+pname+"&id="+str(pid))
    else:
        context={'error':"所有选项不能为空！"}
        return render(request,"editVersion.hml",context)
def delVersion(request):
    vid=request.GET['vid']
    vinfo = Version.objects.get(id=vid)
    pid = vinfo.project_id
    pinfo = Project.objects.get(id=pid)
    pname = pinfo.name
    Version.objects.filter(id=vid).delete()
    user=request.session.get("username","")
    return HttpResponseRedirect("/queryVersion/?user="+user+"&name="+pname+"&id="+str(pid))
def searchp(request):
    query_text=request.GET['search']
    if(query_text==""):
        projectInfo=Project.objects.all()
        # contex={"error":"请输入搜索字符"}
        return HttpResponseRedirect("/broadcast",projectInfo)
    else:
        username = request.session.get('username', '')
        projectInfo=Project.objects.filter(Q(name__icontains=query_text)|Q(description__icontains=query_text) |Q(createTime__icontains=query_text)|Q(endTime__icontains=query_text))
        paginator=Paginator(projectInfo,10)
        page=request.GET.get("page",1)
        curpage=int(page)
        try:
            projectInfo=paginator.page(curpage)
        except PageNotAnInteger:
            projectInfo=paginator.page(1)
        except EmptyPage:
            projectInfo=paginator.page(paginator.num_pages)
        contex={'projects':projectInfo,'username':username}
        return render(request,"broadcast.html",contex)
def searchv(request):
    query_text=request.GET['search']
    pname=request.GET['projectname']
    username = request.session.get("username", "")
    pinfo=Project.objects.get(name=pname)
    pid=pinfo.id
    versionInfo=Version.objects.filter(project_id=pid)
    if(query_text==""):
        context={"projectname":pname,'versions':versionInfo,'user':username}
        return render(request,"queryVersion.html",context)
    else:
        versionInfo=Version.objects.filter(project_id=pid).filter(Q(version__icontains=query_text)|Q(description__icontains=query_text)|Q(release__icontains=query_text)|Q(createtime__icontains=query_text)|Q(endtime__icontains=query_text)|Q(Criticalbugs__icontains=query_text)|Q(Majorbugs__icontains=query_text))
        return render(request,"queryVersion.html",{'versions':versionInfo,'user':username,'projectname':pname})