from django.db import models
from .project_models import Project
from django import forms
from django.utils import timezone
# Create your models here.

class Module(models.Model):
    name=models.CharField(max_length=20)
    description=models.TextField(max_length=50)
    createTime = models.DateTimeField(max_length=20,default=timezone.now)
    endTime=models.DateTimeField(max_length=20)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

