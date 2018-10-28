from ..models.project_models import Project,Version
from django import forms


# Create your models here.
class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields="__all__"
        # fields=['name','description','createTime','status','endTime']
    # def clean_name(self):
    #     name=self.cleaned_data['name']
    #     print("name:"+name)
    #     if(name==""):
    #         raise forms.ValidationError('project name is required', code='proName error')

class VerForm(forms.ModelForm):
    class Meta:
        model=Version
        fields="__all__"
        # fields=['version','description','release','createtime','endtime','Criticalbugs','Majorbugs']
    # def clean_version(self):
    #     version=self.cleaned_data['version']
    #     if(version==""):
    #         raise forms.ValidationError("version is required",code="version error")