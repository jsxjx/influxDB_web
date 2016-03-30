# coding:utf-8
from django.db import models

# Create your models here.

class Stencil(models.Model):
    NAME = models.CharField(max_length = 100)
    WQAR_737_7 = models.CharField(max_length = 1000)
    WQAR_737_3C =  models.CharField(max_length = 1000)
    ATA = models.IntegerField()
    CREATOR = models.CharField(max_length = 100)
    echarts_737_7 = models.CharField(max_length = 1000)
    echarts_737_3C = models.CharField(max_length = 1000)
    def __unicode__(self):              # __str__ on Python 3
        return self.NAME