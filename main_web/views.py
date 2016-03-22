# coding:utf-8
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from decode_all_function import MERGE_DECODE_LIST


import time,datetime
import socket

def home(request):
    return render(request, 'home.html')

def storing_data(request):

    return HttpResponse("已完成数据存入")
