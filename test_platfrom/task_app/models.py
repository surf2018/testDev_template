from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from project_app.models.project_models import Project
from project_app.models.module_models import Module
from interface_app.models import Case
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cases=models.TextField(max_length=1000,default='')
    status=models.CharField(max_length=10,default=0) # 0未执行 、1 执行中，2 执行结束
    result=models.CharField(max_length=10,default=0) #NG 不通过，OK通过
    create_user=models.ForeignKey(User,on_delete=models.CASCADE)
    create_time=models.DateTimeField("创建时间",auto_now_add=True)
    def __str__(self):
        return self.name


# Create your models here.
