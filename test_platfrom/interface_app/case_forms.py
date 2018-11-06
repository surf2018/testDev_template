from .models import Case
from django import forms


# Create your models here.
class CaseForm(forms.ModelForm):
    class Meta:
        model=Case
        exclude=['create_time']