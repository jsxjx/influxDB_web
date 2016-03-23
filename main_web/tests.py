# coding:utf-8
from django.test import TestCase

# Create your tests here.
from hbase_function import HBASE_interface
from main_web.models import Stencil
from django.http import HttpResponse

def import_stencil_hbase(request):
    hb_if = HBASE_interface()
    connection = hb_if.connect_hbase
    table_tablename_index = connection.table("stencil_config")
    print table_tablename_index.scan()
    for key, data in table_tablename_index.scan():
        print key
        if not Stencil.objects.all().filter(NAME = data['c1:NAME']).exists():
            Stencil.objects.get_or_create(
            NAME = data['c1:NAME'],
            WQAR_737_7 = data['c1:WQAR512_IDC'],
            WQAR_737_3C =  data['c1:WQAR256_IDC'],
            ATA = data['c1:ATA'],
            CREATOR = data['c1:creator'],
            echarts_737_7 = data['c1:ECHARTS_512'],
            echarts_737_3C = data['c1:ECHARTS_256'])
            print u"已录入"
        else:
            print u"已存在模版"

    return HttpResponse("已完成数据存入")
