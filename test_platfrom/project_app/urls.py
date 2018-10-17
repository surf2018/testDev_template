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
    path('editProject/<int:pid>/',views.editProject),
    path('editP_action/<int:pid>/',views.editP_action),
    path('delProject/<int:pid>/',views.delProject),
    path('createVersion/<int:pid>/<str:pname>/vcreate/', views.createVersion),
    path('createV_acton/<int:pid>/', views.createV_acton),
    path('editVersion/<int:vid>/',views.editVersion),
    path('editV_acton/<int:vid>/',views.editV_action),
    path('delVersion/<int:vid>/',views.delVersion),
    path('searchp/',views.searchp),
    path("searchv/",views.searchv),

]
