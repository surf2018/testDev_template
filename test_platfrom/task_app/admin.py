from django.contrib import admin
from .models import Task
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name","description","status","result","create_time"]
admin.site.register(Task,TaskAdmin)

# Register your models here.
