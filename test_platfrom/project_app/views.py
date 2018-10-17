from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import Project, Version
from .forms import ProjectForm, VerForm
from django.db.models import Q


# Create your views here.
#
@login_required
def dashboard(request):
    # username=request.COOKIES.get('username','')
    username = request.session.get('username', '')
    type = request.GET['type']
    if (type == ''):
        type = 'plist'
    # projects=Project.objects.all()
    projects = Project.objects.get_queryset().order_by('id')
    # 分页
    paginator = Paginator(projects, 10)
    page = request.GET.get('page', 1)
    curpage = int(page)
    try:
        print(page)
        projects = paginator.page(curpage)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    context = {'username': username, 'projects': projects, 'type': type}
    if (type == 'pcreate'):
        form = ProjectForm()
        context = {'username': username, 'projects': projects, 'type': type, 'form': form}
    elif (type == 'vlist'):
        pid = request.GET['pid']
        request.session['pid'] = pid
        project = Project.objects.get(id=pid)
        pname = project.name
        request.session['pname'] = pname
        verinfos = Version.objects.filter(project_id=pid)
        # versions =Version.objects.get_queryset().order_by('id')
        # 分页
        paginator = Paginator(verinfos, 10)
        page = request.GET.get('page', 1)
        curpage = int(page)
        try:
            print(page)
            verinfos = paginator.page(curpage)
        except PageNotAnInteger:
            verinfos = paginator.page(1)
        except EmptyPage:
            verinfos = paginator.page(paginator.num_pages)
        context = {'verinfos': verinfos, 'type': type, 'pname': pname, 'pid': pid, 'username': username}
    # query databases dispaly all projects
    return render(request, 'project/broadcast.html', context)


def createP_action(request):
    if (request.method != 'POST'):
        form = ProjectForm()
    else:
        form = ProjectForm(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect("/project/dashboard?type=plist")


def createVersion(request):
    pname = request.GET['pname']
    pid = request.GET['pid']
    form = VerForm()
    type = 'vcreate'
    usename = request.session.get('username', '')
    context = {'projectname': pname, 'form': form, 'type': type, 'pid': pid, 'username': usename}
    return render(request, "project/broadcast.html", context)


def createV_acton(request):
    # 写入数据
    pid = request.GET['pid']
    if (request.method != 'POST'):
        form = VerForm()
    else:
        form = VerForm(request.POST)
        if (form.is_valid()):
            form.instance.project_id = pid
            form.save()
            return HttpResponseRedirect("/project/dashboard?type=vlist&pid=" + pid)


def editProject(request):
    pname = request.GET['name']
    pid = request.GET['id']
    pro = Project.objects.get(id=pid)
    form = ProjectForm(instance=pro)
    type = 'editp'
    username = request.session.get('username', '')
    context = {'pid': pid, 'projectname': pname, 'form': form, 'type': type, 'username': username}
    return render(request, "project/broadcast.html", context)


def editP_action(request):
    # 数据库中更新数据
    if (request.method != 'POST'):
        form = ProjectForm()
    else:
        pid = request.GET['pid']
        pro = Project.objects.get(id=pid)
        form = ProjectForm(request.POST, instance=pro)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect("/project/dashboard?type=plist")


def delProject(request):
    # name=request.GET['name']
    id = request.GET['id']
    # 删除数据库
    Project.objects.filter(id=id).delete()
    return HttpResponseRedirect("/project/dashboard?type=plist")


def editVersion(request):
    vid = request.GET['vid']
    # query数据库
    verInfo = Version.objects.get(id=vid)
    form = VerForm(instance=verInfo)
    type = 'editv'
    username = request.session.get('username', '')
    context = {'versionInfo': verInfo, 'form': form, 'type': type, 'username': username}
    return render(request, "project/broadcast.html", context)


def editV_action(request):
    if (request.method != 'POST'):
        form = ProjectForm()
    else:
        vid = request.GET['vid']
        verinfo = Version.objects.get(id=vid)
        pid = verinfo.project_id
        pro = Project.objects.get(id=pid)
        pname = pro.name
        form = VerForm(request.POST, instance=verinfo)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect("/project/dashboard?type=vlist&pname=" + pname + "&pid=" + str(pid))


def delVersion(request):
    vid = request.GET['vid']
    vinfo = Version.objects.get(id=vid)
    pid = vinfo.project_id
    pinfo = Project.objects.get(id=pid)
    pname = pinfo.name
    Version.objects.filter(id=vid).delete()
    user = request.session.get("username", "")
    return HttpResponseRedirect("/project/dashboard?type=vlist&pname=" + pname + "&pid=" + str(pid))


def searchp(request):
    query_text = request.GET['search']
    if (query_text == ""):
        projectInfo = Project.objects.all()
        # contex={"error":"请输入搜索字符"}
        return HttpResponseRedirect("/project/dashboard/?type=plist", projectInfo)
    else:
        username = request.session.get('username', '')
        projectInfo = Project.objects.filter(Q(name__icontains=query_text) | Q(description__icontains=query_text))
        paginator = Paginator(projectInfo, 10)
        page = request.GET.get("page", 1)
        curpage = int(page)
        try:
            projectInfo = paginator.page(curpage)
        except PageNotAnInteger:
            projectInfo = paginator.page(1)
        except EmptyPage:
            projectInfo = paginator.page(paginator.num_pages)
        context = {'projects': projectInfo, 'username': username, 'type': 'plist'}
        return render(request, "project/broadcast.html", context)


def searchv(request):
    query_text = request.GET['search']
    # url=request.get_full_path()
    pname = request.session.get('pname', '')
    pid = request.session.get('pid', '')
    username = request.session.get("username", "")
    type = 'vlist'
    versionInfo = Version.objects.filter(project_id=pid)
    if (query_text == ""):
        context = {'versions': versionInfo, 'user': username}
        return HttpResponseRedirect("/project/dashboard/?type=vlist&pname=" + pname + "&pid=" + str(pid), context)
    else:
        versionInfo = Version.objects.filter(project_id=pid).filter(
            Q(version__icontains=query_text) | Q(description__icontains=query_text))
        print("versionInfo:" + str(versionInfo))
        context = {'verinfos': versionInfo, 'user': username, 'pname': pname, 'type': type, "pid": pid, 'type': 'vlist'}
        return render(request, "project/broadcast.html", context)
# Create your views here.
