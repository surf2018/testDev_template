from ..interface_app.models import Case
from django import forms


# Create your models here.
class ModuleForm(forms.ModelForm):
    class Meta:
        model=Case
        fields=["name","name","url","method","type"]