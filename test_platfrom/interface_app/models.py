# Create your models here.
import sys
sys.path.insert(0, '..')
from django.db import models
from ...test_platfrom.project_app.models.project_models import Project
from ..project_app.models.module_models import Module

class Case(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=100)
    method = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    header = models.CharField(max_length=200)
    data = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    model = models.ForeignKey(Module, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

