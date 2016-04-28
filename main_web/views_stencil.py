#coding=utf-8
import json

from django.http import HttpResponse
from django.shortcuts import render

from list2string_and_echarts_function import LIST_to_STR
from main_web.models import Stencil


def storing_stencil(request):
    return render(request, 'storing_stencil_html.html')

def storing_stencil_ajax(request):
    #前端传入参数
    ata = request.GET.get('stencil_ATA', None)
    name = request.GET.get('stencil_name', None)
    para_256 = request.GET.get('stencil_256_para', None)
    para_512 = request.GET.get('stencil_512_para', None)
    creator = request.GET.get('stencil_creator', None)
    #对传入进行解码
    name_decode = name.encode('utf-8')
    creator_decode = creator.encode('utf-8')
    para_256_decode = para_256.split(',')
    para_512_decode = para_512.split(',')
    #防输错设计，前端多输入了，号，列表中有空值即去掉
    while '' in para_256_decode:
        para_256_decode.remove('')
    while '' in para_512_decode:
        para_512_decode.remove('')

    list_str = LIST_to_STR()

    str_stencil_name = name_decode
    str_para_256 = list_str.int_to_str(para_256_decode)
    str_para_512 = list_str.int_to_str(para_512_decode)

    if not Stencil.objects.all().filter(NAME = str_stencil_name).exists():
        Stencil.objects.get_or_create(
        NAME = str_stencil_name,
        WQAR_737_7 = str_para_512,
        WQAR_737_3C =  str_para_256,
        ATA = ata,
        CREATOR = creator_decode,
        echarts_737_7 = ';;',
        echarts_737_3C = ';;')

        #回传前端，反馈结果
        para_256_post = ','.join(para_256_decode)
        para_512_post = ','.join(para_512_decode)
        text = '<br>已录入<br>模版：' + str(name_decode) + \
               '<br>参数256：' + str(para_256_post) + \
                '<br>参数512：' + str(para_512_post) + \
               '<br>章节：' + str(ata)
    else:
        text = '已存在同名模版,请重新命名'
    return HttpResponse(text)


def stencil_list(request):

    list_str = LIST_to_STR()
    tablename = "stencil_config"
    cf_set = ['c1:NAME',
              'c1:ATA',
              'c1:creator',
              ]

    stencil_dic = Stencil.objects.all()
    dic_index = {}
    list_index = []
    for item in stencil_dic:
        dic_index = {
            'NAME':item.NAME,
            'ATA':item.ATA,
            'creator':item.CREATOR
        }
        list_index.append(dic_index)
    post_json = json.dumps(list_index)

    return render(request, 'stencil_list.html',{'result_json': post_json})

def edit_stencil(request, stencil_NAME):

    list_str = LIST_to_STR()
    result_scan_dict = Stencil.objects.get(NAME = stencil_NAME)


    dic_index = {
            'NAME':result_scan_dict.NAME,
            'ATA':result_scan_dict.ATA,
            'CREATOR':result_scan_dict.CREATOR,
             'WQAR_737_7':result_scan_dict.WQAR_737_7,
            'WQAR_737_3C':result_scan_dict.WQAR_737_3C
        }
    reslut_json = json.dumps([dic_index])

    list_WQAR256_model = list_str.str_to_int(result_scan_dict.WQAR_737_3C)
    list_WQAR512_model = list_str.str_to_int(result_scan_dict.WQAR_737_7)
    list_WQAR256_para_index, list_WQAR512_para_index = list_str.make_para_id_list()
    result_list_256_id = []
    result_list_512_id = []
    for each_id_number in list_WQAR256_model:
        result_list_256_id.append(list_WQAR256_para_index[int(each_id_number)])
    for each_id_number in list_WQAR512_model:
        result_list_512_id.append(list_WQAR512_para_index[int(each_id_number)])

    print result_list_256_id,result_list_512_id

    return render(request, 'edit_stencil.html',{'result_json': reslut_json,
                                                'result_json_256':result_list_256_id,
                                                'result_json_512':result_list_512_id,
                                                'stencil_NAME':stencil_NAME})

def stencil_echarts(request):

    stencil_NAME = request.GET.get('stencil_NAME', None)
    post_string_737_3C = request.GET.get('post_string_256', None)
    post_string_737_7 = request.GET.get('post_string_512', None)

    singel_stencil = Stencil.objects.get(NAME = stencil_NAME)
    singel_stencil.echarts_737_7 = post_string_737_7
    singel_stencil.echarts_737_3C = post_string_737_3C
    singel_stencil.save()
    return HttpResponse("已录入")
