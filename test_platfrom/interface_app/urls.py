"""test_platfroms URL Configuration

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
from interface_app.views import testcase_views
from interface_app.views import testcase_api
# from project_app import views

urlpatterns = [
    path('case_manager/',testcase_views.caselist),
    path('debug_ajax/',testcase_api.debug_ajax),
    path('save/',testcase_api.saveDate),
    path('seletAjax/',testcase_api.selectAjax),
    path('debugCase/<int:caseid>/',testcase_views.debugCase),
    path('update/',testcase_api.updateDate),
    path('delCase/<int:caseid>/',testcase_views.delCase),
    path('searchcase/',testcase_views.searchCase),
    path('queryCase/',testcase_api.queryCaseAjax),
    path('assert/',testcase_api.assertResult),

]
