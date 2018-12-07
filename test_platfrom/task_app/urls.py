"""test_platfrom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task_app.views import task_views,task_api
# from project_app import views

urlpatterns = [
    path('task_manager/',task_views.tasklist),
    path('save/',task_api.save),
    path('seletAjax/',task_api.selectAjax),
    path('delTask/<int:taskid>/',task_views.delTask),
    path('editTask/<int:taskid>/',task_views.editTask),
    path('queryTask/',task_api.queryTask),

]
