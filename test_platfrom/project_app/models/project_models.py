from django.db import models
from django import forms
from django.utils import timezone
# Create your models here.
class Project(models.Model):
    # pid=models.IntegerField(default=)
    name=models.CharField(max_length=20)
    description=models.CharField(max_length=50)
    createTime=models.DateField(max_length=20)
    status=models.BooleanField("status",default=True)
    endTime=models.DateField(max_length=20)
    def __str__(self):
        return self.name

class Version(models.Model):
    version=models.CharField(max_length=20)
    description=models.CharField(max_length=20)
    release=models.BooleanField("release",default=False)
    createtime = models.DateField(max_length=20)
    endtime=models.DateField(max_length=20)
    Criticalbugs=models.CharField(max_length=20,default='0')
    Majorbugs=models.CharField(max_length=20,default='0')
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    def __str__(self):
        return self.version