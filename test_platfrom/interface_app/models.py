# Create your models here.
import sys
from django.db import models
from django.contrib.auth.models import User
from project_app.models.project_models import Project
from project_app.models.module_models import Module
class Case(models.Model):
    name = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    method = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    header = models.CharField(max_length=1000)
    data = models.CharField(max_length=1000)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    model=models.ForeignKey(Module,on_delete=models.CASCADE)
    status=models.BooleanField("status",default=True)
    response_assert=models.CharField(max_length=1000)
    create_user=models.ForeignKey(User,on_delete=models.CASCADE)
    create_time=models.DateTimeField("创建时间",auto_now_add=True)
    def __str__(self):
        return self.name

