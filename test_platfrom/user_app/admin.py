from django.contrib import admin
from .models import Project,Version
# Register your models here.
#自带一个admin后台
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name","status","createTime","endTime"]
class VersionAdmin(admin.ModelAdmin):
    list_display = ["version","release","project_id","createtime","endtime","Criticalbugs","Majorbugs"]
admin.site.register(Project,ProjectAdmin)
admin.site.register(Version,VersionAdmin)