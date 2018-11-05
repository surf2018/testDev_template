# Create your models here.
import sys
from django.db import models
sys.path.append("..project_app")
class Case(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    method = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    header = models.CharField(max_length=200)
    data = models.CharField(max_length=200)
    def __str__(self):
        return self.name

