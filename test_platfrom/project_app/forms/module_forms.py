from ..models.module_models import Module
from django import forms


# Create your models here.
class ModuleForm(forms.ModelForm):
    class Meta:
        model=Module
        fields="__all__"