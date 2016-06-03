# coding:utf-8
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from influxdb_function import influxDB_interface


def home(request):
    infdb_if = influxDB_interface()
    sector_index = infdb_if.limit_query("DB_sector_index", "*", "index")
    df = sector_index['index']
    result_json = df.to_json(orient="records")
    return render(request, 'home.html',{'result_json': result_json})
