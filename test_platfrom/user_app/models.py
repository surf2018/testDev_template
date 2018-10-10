from django.db import models
from django.utils import timezone

# Create your models here.
#ORM create database able
#create project database
class Project(models.Model):
    # pid=models.IntegerField(default=)
    name=models.CharField(max_length=20)
    description=models.TextField(max_length=50)
    createTime=models.CharField(max_length=20)
    status=models.BooleanField("status:",default=True)
    endTime=models.CharField(max_length=20,default="2099-12-30")
    def __unicode__(self):
        return self.name

class Version(models.Model):
    version=models.CharField(max_length=20)
    description=models.TextField(max_length=50)
    release=models.CharField(max_length=5)
    createtime = models.CharField(max_length=20,default='')
    endtime=models.CharField(max_length=20,default="2099-12-30")
    Criticalbugs=models.CharField(max_length=20,default='0')
    Majorbugs=models.CharField(max_length=20,default='0')
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    def __unicode__(self):
        return self.version