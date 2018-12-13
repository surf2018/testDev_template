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
from project_app.views import project_views
from project_app.views import module_views
# from project_app import views

urlpatterns = [
    path('dashboard/',project_views.dashboard),
    path('modulelist/',module_views.dashboard),

    path('createP_action/',project_views.createP_action),
    path('createM_action/', module_views.createM_action),

    path('editProject/<int:pid>/',project_views.editProject),
    path('editModule/<int:mid>/',module_views.editModule),

    path('editP_action/<int:pid>/',project_views.editP_action),
    path('editM_action/<int:mid>/',module_views.editM_action),

    path('delProject/<int:pid>/',project_views.delProject),
    path('delModule/<int:mid>/',module_views.delModule),

    path('createVersion/<int:pid>/<str:pname>/vcreate/', project_views.createVersion),
    path('createV_acton/<int:pid>/', project_views.createV_acton),
    path('editVersion/<int:vid>/',project_views.editVersion),
    path('editV_acton/<int:vid>/',project_views.editV_action),
    path('delVersion/<int:vid>/',project_views.delVersion),
    path('searchp/',project_views.searchp),
    path("searchv/",project_views.searchv),
    path("searchm/",module_views.searchm),


]
