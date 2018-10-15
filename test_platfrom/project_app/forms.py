from .models import Project,Version
from django import forms
from django.utils import timezone
# Create your models here.
class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=['name','description','createTime','status','endTime']

class VerForm(forms.ModelForm):
    class Meta:
        model=Version
        fields=['version','description','release','createtime','endtime','Criticalbugs','Majorbugs']