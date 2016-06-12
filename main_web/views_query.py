# coding:utf-8
import json

from django.http import HttpResponse
from django.shortcuts import render

from aircraft_config import AC_WQAR_CONFIG
from list2string_and_echarts_function import Echarts_option
from list2string_and_echarts_function import LIST_to_STR
from influxdb_function import influxDB_interface
from main_web.models import Stencil
from arrow_time import today_date_for_influxd_sql
from arrow_time import ten_day_ago_for_influxd_sql

def all_childtable_index_list(request):
    if request.method == 'POST':
        post_data = request.POST
        date_range = post_data["date_range"]
        date_start = date_range.split(' to ')[0]
        date_end = date_range.split(' to ')[1]

    else:
        date_start = today_date_for_influxd_sql()
        date_end = today_date_for_influxd_sql()

    where_str = " WHERE time > " + "'" + date_start + "'" + " - 8h" + " AND time < " + "'" + date_end + "'" + " + 16h"
    infdb_if = influxDB_interface()
    sector_index = infdb_if.inf_query("DB_sector_index", "*", "index", where_str)
    if sector_index <> {}:
        df = sector_index['index']
        result_json = df.to_json(orient="records")
        return render(request, 'all_childtable_index_list.html', {'result_json': result_json,
                                                                  'date_start': date_start,
                                                                  'date_end': date_end})
    else:
        return render(request, 'all_childtable_index_list.html', {'date_start': date_start,
                                                                  'date_end': date_end + "  no data"})


def query_index(request):
    if request.method == 'POST':
        post_data = request.POST
        if post_data["date_start"]=='' or post_data["date_end"] == '':
            date_start = ten_day_ago_for_influxd_sql()
            date_end = today_date_for_influxd_sql()
        else:
            date_start = post_data["date_start"]
            date_end = post_data["date_end"]
        AC_id = post_data["AC_id"]
        where_str = " WHERE time > " + "'" + date_start + "'" + " AND time < " + "'" + date_end + "'" + " + 1d" + " AND AC=" + "'" + AC_id + "'"
        infdb_if = influxDB_interface()
        sector_index = infdb_if.inf_query("DB_sector_index", "*", "index", where_str)
        if sector_index <> {}:
            df = sector_index['index']
            result_json = df.to_json(orient="records")
            return render(request, 'single_plane_query.html', {'result_json': result_json,
                                                               'date_start': date_start,
                                                               'date_end': date_end,
                                                               'AC_id': AC_id})
        else:
            return render(request, 'single_plane_query.html', {'date_start': date_start,
                                                               'date_end': date_end + "  no data",
                                                               'AC_id': AC_id})
    else:
        return render(request, 'single_plane_query.html')

def runup_list(request):
    infdb_if = influxDB_interface()
    sector_index = infdb_if.inf_query("DB_sector_index", "*", "index", " WHERE FLT_status='GROUND' ")
    df = sector_index['index']
    result_json = df.to_json(orient="records")
    return render(request, 'all_childtable_index_list.html',{'result_json': result_json})

def tendency_total(request):
    if request.method == 'POST':
        post_data = request.POST
        date_range = post_data["date_range"]
        date_start = date_range.split(' to ')[0]
        date_end = date_range.split(' to ')[1]
        tendency_type = post_data["tendency_type"]

        where_str = " WHERE time > " + "'" + date_start + "'" + " AND time < " + "'" + date_end + "'" + " + 1d"
        infdb_if = influxDB_interface()
        sector_index = infdb_if.inf_query("tendency", "*", tendency_type, where_str)
        if sector_index <> {}:
            df = sector_index[tendency_type]
            result_json = df.to_json(orient="records")
            return render(request, 'tendency_total.html', {'result_json': result_json,
                                                               'date_start': date_start,
                                                               'date_end': date_end,
                                                               })
        else:
            return render(request, 'tendency_total.html', {'date_start': date_start,
                                                               'date_end': date_end + "  no data",
                                                               })
    else:
        date_start = ten_day_ago_for_influxd_sql()
        date_end = today_date_for_influxd_sql()
        where_str = " WHERE time > " + "'" + date_start + "'" + " AND time < " + "'" + date_end + "'" + " + 1d"
        infdb_if = influxDB_interface()
        sector_index = infdb_if.inf_query("tendency", "*", "tendency_total", where_str)
        df = sector_index['tendency_total']
        result_json = df.to_json(orient="records")
        return render(request, 'tendency_total.html', {'result_json': result_json,
                                                                  'date_start': date_start,
                                                                  'date_end': date_end})

def tendency_single(request):
    if request.method == 'POST':
        post_data = request.POST
        date_range = post_data["date_range"]
        date_start = date_range.split(' to ')[0]
        date_end = date_range.split(' to ')[1]
        para_name = post_data["para_name"]
        para_name_sed = "\"" + para_name + "\""
        exclude_list = ["AC","AC_sector","FLT_number","FLT_status","update_date","update_time"]
        exclude_list = map(lambda x:"\"" + x + "\"", exclude_list)
        exclude_list.append(para_name_sed)
        query_para = ",".join(exclude_list)
        print query_para
        AC_id = post_data["AC_id"]
        AC_id_sed = "\'" + AC_id + "\'"
        qar_conf = AC_WQAR_CONFIG().juge_config(AC_id)
        if qar_conf == "737_7":
            tendency_type = "tendency_737_7"
        elif qar_conf == "737_3C":
            tendency_type = "tendency_737_3C"
        where_str = " WHERE AC = " + AC_id_sed + " AND " + "time > " + "'" + date_start + "'" + " AND time < " + "'" + date_end + "'" + " + 1d"
        infdb_if = influxDB_interface()
        sector_index = infdb_if.inf_query("tendency", query_para, tendency_type, where_str)
        if sector_index <> {}:
            df = sector_index[tendency_type]
            result_json = df.to_json(orient="records")
            return render(request, 'tendency_single.html', {'result_json': result_json,
                                                               'date_start': date_start,
                                                               'date_end': date_end,
                                                               })
        else:
            return render(request, 'tendency_single.html', {'date_start': date_start,
                                                               'date_end': date_end + "  no data",
                                                               })
    else:
        return render(request, 'tendency_single.html', {'result_json': {}})

def tendency_single_para_list(request):
    AC_id = request.GET.get('AC_id', None)
    qar_conf = AC_WQAR_CONFIG().juge_config(AC_id)
    if qar_conf == "737_7":
        mes = "tendency_737_7"
    elif qar_conf == "737_3C":
        mes = "tendency_737_3C"
    para_object = influxDB_interface().show_fields("tendency", mes)

    para_list = []
    exclude_list = ["AC","AC_sector","FLT_number","FLT_status","update_date","update_time"]
    for item in para_object:
        para_name = item['fieldKey']
        if para_name not in exclude_list:
            para_list.append(para_name)
    para_json = json.dumps(para_list)
    return HttpResponse(para_json)

def childtable(request, sector_id):
    result_list = []

    query_stencil = Stencil.objects.all()
    for item in query_stencil:
        dic_index = {
            'NAME':item.NAME
        }
        result_list.append(dic_index)

    return render(request, 'childtable.html', {'sector_id': sector_id,
                                               'stencil_option': result_list})

def ajax_some_para(request):
    list_str = LIST_to_STR()
    post_NAME = request.GET.get('value_conf', None)
    print post_NAME
    post_flight_id = request.GET.get('flight_id', None)
    print post_flight_id
    aircraft_id = post_flight_id[0:6]

    #获取模版内参数列表
    stencil_object = Stencil.objects.get(NAME = post_NAME)

    list_3C, list_7 = LIST_to_STR().make_para_id_list()
    list_units_3C, list_units_7 = LIST_to_STR().make_para_units_list()
    list_WQAR256 = list_str.str_to_int(stencil_object.WQAR_737_3C)
    list_WQAR512 = list_str.str_to_int(stencil_object.WQAR_737_7)
    ac_wqar_config = AC_WQAR_CONFIG()

    echarts_option_256 = stencil_object.echarts_737_3C
    echarts_option_512 = stencil_object.echarts_737_7
    dic_units = {}
    list_para_name = []
    if aircraft_id in ac_wqar_config.WQAR_7_SERISE_list:
        model = list_WQAR512
        list_units = list_units_7
        ac_conf = '737_7'
        for item in model:
            list_para_name.append(list_7[int(item)])
            dic_units[list_7[int(item)] ]= list_units[int(item)]
        str_echarts_option = echarts_option_512
    elif aircraft_id in ac_wqar_config.WQAR_3C_SERISE_list:
        model = list_WQAR256
        list_units = list_units_3C
        ac_conf = '737_3C'
        for item in model:
            list_para_name.append(list_3C[int(item)])
            dic_units[list_3C[int(item)] ]= list_units[int(item)]
        str_echarts_option = echarts_option_256
    else:
        return HttpResponse("无此机号")



    print list_para_name
    query_result = influxDB_interface().list_query(
        "CKG_QAR",
        list_para_name,
        ac_conf,
        post_flight_id)
    query_result.index = range(1,(len(query_result.index)+1),1)
    new_df = query_result.fillna('-')
    list_c1_c2 = new_df.to_dict(orient="records")
    para_name_dic = {}

    for key in list_c1_c2[0]:
        para_name_dic[key] = key

    list_c1_c2.insert(0, para_name_dic)
    list_c1_c2.append(dic_units) # 单位暂时不加上,待填坑

    # 传递echarts设置信息
    ec_op = Echarts_option()
    echarts_config_option = ec_op.str_to_obj(str_echarts_option)
    # 得出echarts_option中的逻辑值参数表列表
    list_index_of_logic_echarts = ec_op.judge_logic_echart(echarts_config_option)

    result_json = json.dumps([list_c1_c2, echarts_config_option, list_index_of_logic_echarts])
    return HttpResponse(result_json)