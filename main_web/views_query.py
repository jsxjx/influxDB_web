# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse


from aircraft_config import AC_WQAR_CONFIG
from hbase_function import Echarts_option
from influxdb_function import influxDB_interface
import json

def all_childtable_index_list(request):
    infdb_if = influxDB_interface()
    sector_index = infdb_if.inf_query("DB_sector_index", "*", "index")
    df = sector_index['index']
    result_json = df.to_json(orient="records")
    return render(request, 'all_childtable_index_list.html',{'result_json': result_json})

def childtable(request, sector_id):
    result_list = [{
        'index' : '001',
        'NAME' : 'EGT'
    }]
    return render(request, 'childtable.html', {'sector_id': sector_id,
                                               'stencil_option': result_list})

def ajax_some_para(request):

    post_index = request.GET.get('value_conf', None)
    print post_index
    post_flight_id = request.GET.get('flight_id', None)
    print post_flight_id
    aircraft_id = post_flight_id[0:6]

    query_result = influxDB_interface().list_query("CKG_QAR",["623:STBY HYD OIL PRESSURE","463:GUIDANCE CUE X POSITION"],'737_7', 'B-1527_20150901023317')
    query_result.index = range(1,(len(query_result.index)+1),1)
    new_df = query_result.fillna('-')
    list_c1_c2 = new_df.to_dict(orient="records")
    para_name_dic = {}
    para_unit_dic = {}
    for key in list_c1_c2[0]:
        para_name_dic[key] = key
        para_unit_dic[key] = ''
    list_c1_c2.insert(0, para_name_dic)
    list_c1_c2.append(para_unit_dic) # 单位暂时不加上,待填坑
    echarts_config_option = []
    list_index_of_logic_echarts = []
    result_json = json.dumps([list_c1_c2, echarts_config_option, list_index_of_logic_echarts])
    return HttpResponse(result_json)