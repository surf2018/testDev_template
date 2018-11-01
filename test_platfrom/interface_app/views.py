from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

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
    method=


# Create your views here.
