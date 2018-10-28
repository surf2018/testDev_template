from ..models.module_models import Module
from django import forms


# Create your models here.
class ModuleForm(forms.ModelForm):
    class Meta:
        model=Module
        fields=['name','description','createTime','endTime','project']
    def clean_name(self):
            modName = self.cleaned_data['name']
            if(modName==""):
                raise forms.ValidationError("module name is require",code="module error")