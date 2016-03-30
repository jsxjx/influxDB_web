#!/home/hadoop/anaconda2/bin/python2.7
#coding=utf-8
'''
    ftp增量下载
'''
import time
import shutil

from django.http import HttpResponse
from django.shortcuts import render
from main_web.FTP_downloadfiles import TXT_FTP_INFO
from main_web.FTP_downloadfiles import FTP_DOWNLOAD_APPEND_FILES
from main_web.save_QAR_use_pandas import PUT_DATA


def sync_and_decode(request):
    FTP_get = FTP_DOWNLOAD_APPEND_FILES()
    FTP_get.get_append_files()

    get_ftp_info = TXT_FTP_INFO()
    ftp_info_list = get_ftp_info.read()

    hostaddr = ftp_info_list[0] # ftp地址
    username = ftp_info_list[1] # 用户名
    password = ftp_info_list[2] # 密码
    rootdir_local = ftp_info_list[3] #本地增量下载目录


    PUT_DATA().put()
    shutil.rmtree(rootdir_local)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return HttpResponse(u"%s 从工程部同步一次数据，并译码" % time_str)