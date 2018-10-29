from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from ..forms.module_forms import ModuleForm
from ..models.module_models import Module
from ..models.project_models import Project

from django.db.models import Q


# Create your views here.
#
@login_required
def dashboard(request):
    username = request.session.get('username', '')
    type = request.GET['type']
    if (type == ''):
        type = 'mlist'
    pNameList={}
    # projects=Project.objects.all()
    modules = Module.objects.all()
    # projects=Module.objects.select_related("project").all()
    # for m in modules:
    #     pNameList[p.id] = p.project.name
    # print(projects[0].project.name)
    # 分页
    paginator = Paginator(modules, 10)
    page = request.GET.get('page', 1)
    curpage = int(page)
    try:
        print(page)
        modules = paginator.page(curpage)
    except PageNotAnInteger:
        modules = paginator.page(1)
    except EmptyPage:
        modules = paginator.page(paginator.num_pages)
    context = {'username': username, 'modules': modules, 'type': type}
    #"pName": pNameList
    if(type == 'mcreate'):
        form = ModuleForm()
        context = {'username': username,'type': type, 'form': form}
    return render(request, 'project/module.html', context)


def createM_action(request):
    if (request.method != 'POST'):
        form = ModuleForm()
        return HttpResponseRedirect("/module/modulelist?type=mlist")
    else:
        form = ModuleForm(request.POST)
        print("moduel valid:"+str(form.is_valid()))
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect("/module/modulelist?type=mlist")


def editModule(request, mid):
    m = Module.objects.get(id=mid)
    form = ModuleForm(instance=m)
    type = 'editm'
    username = request.session.get('username', '')
    context = {'form': form, 'type': type, 'username': username,'mid':mid}
    return render(request, "project/module.html", context)

def editM_action(request, mid):
    # 数据库中更新数据
    if (request.method != 'POST'):
        form = ModuleForm()
    else:
        # pid = request.GET['pid']
        m = Module.objects.get(id=mid)
        form = ModuleForm(request.POST, instance=m)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect("/module/modulelist?type=mlist")

def delModule(request, mid):
    # 删除数据库
    Module.objects.filter(id=mid).delete()
    return HttpResponseRedirect("/module/modulelist?type=mlist")


def searchm(request):
    query_text = request.GET['search']
    if (query_text == ""):
        moduleInfo = Module.objects.all()
        # contex={"error":"请输入搜索字符"}
        return HttpResponseRedirect("/module/modulelist?type=mlist", moduleInfo)
    else:
        username = request.session.get('username', '')
        moduleInfo = Module.objects.filter(Q(name__icontains=query_text) | Q(description__icontains=query_text) |Q(project__name__icontains=query_text))
        paginator = Paginator(moduleInfo, 10)
        page = request.GET.get("page", 1)
        curpage = int(page)
        try:
            moduleInfo = paginator.page(curpage)
        except PageNotAnInteger:
            moduleInfo = paginator.page(1)
        except EmptyPage:
            moduleInfo = paginator.page(paginator.num_pages)
        context = {'modules': moduleInfo, 'username': username, 'type': 'mlist'}
        return render(request, "project/module.html", context)

# Create your views here.
