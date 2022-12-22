# Create your models here.

from django.db import models


class Bottle(models.Model):
    id = models.AutoField(primary_key=True)
    result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.result

class BottleDefect(models.Model):
    id = models.AutoField(primary_key=True)
    bottle = models.ForeignKey(Bottle, on_delete=models.CASCADE)
    defect_name = models.CharField(max_length=100)
    result  = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.defect_name
