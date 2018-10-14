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
from project_app import views
# from project_app import views

urlpatterns = [
    path('dashboard/',views.dashboard),
    path('createP_action/',views.createP_action),
    path('createVersion/',views.createVersion),
    path('createV_acton/',views.createV_acton),
    path('queryVersion/',views.queryVersion),
    path('editProject/',views.editProject),
    path('editP_acton/',views.editP_action),
    path('delProject/',views.delProject),
    path('editVersion/',views.editVersion),
    path('editV_acton/',views.editV_action),
    path('delVersion/',views.delVersion),
    path('search/',views.searchp),
    path("searchV/",views.searchv),

]
