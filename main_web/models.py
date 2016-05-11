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

class RUNUP_TableNameList(models.Model):
    table_name = models.CharField(max_length=20)
    Aircraft_Identification = models.CharField(max_length = 6)
    updata_Date = models.DateField()
    updata_Time = models.CharField(max_length = 8)
    EGT_1_max = models.IntegerField()
    EGT_2_max = models.IntegerField()
    EGT_max = models.IntegerField()
    VIB_L_max = models.DecimalField(max_digits=5, decimal_places=2)
    VIB_R_max = models.DecimalField(max_digits=5, decimal_places=2)
    VIB_max = models.DecimalField(max_digits=5, decimal_places=2)
    SIGN_RUNUP = models.BooleanField()
    SIGN_ENGINE_CLEAN = models.BooleanField()
    FLT_Number = models.CharField(max_length = 8, null=True)