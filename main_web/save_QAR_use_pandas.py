# coding:UTF-8

from influx_decode_all_function import MERGE_DECODE_LIST
from aircraft_config import AC_WQAR_CONFIG
from IP_judge import LOCAL
from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from FLT_tag import FLT_tag
import pandas as pd
import time
from multiprocessing import Pool
import socket
import os

def div_list(ls,n):
    if not isinstance(ls,list) or not isinstance(n,int):
        return []
    ls_len = len(ls)
    if n<=0 or 0==ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = ls_len/n
        k = ls_len%n
        ### j,j,j,...(前面有n-1个j),j+k
        #步长j,次数n-1
        ls_return = []
        for i in xrange(0,(n-1)*j,j):
            ls_return.append(ls[i:i+j])
        #算上末尾的j+k
        ls_return.append(ls[(n-1)*j:])
        return ls_return

def put_data_to_influxDB(list_qar, file_name):
    flt_tag = FLT_tag()
    ac_id = file_name[0:6]
    sector_number = file_name[7:21]
    update_date = sector_number[0:8]
    update_time = sector_number[8:]
    AC_sector = file_name[0:21]

    if ac_id in AC_WQAR_CONFIG().WQAR_3C_SERISE_list:
        measurement_name = "737_3C"
    elif ac_id in AC_WQAR_CONFIG().WQAR_7_SERISE_list:
        measurement_name = "737_7"
    else:
        print u"no ac_id"
        return
    print measurement_name
    FLT_number = flt_tag.get_FTL_number(list_qar[2:],measurement_name)
    list_RADIO_HEIGHT, list_qar[2:] = flt_tag.get_RADIO_HEIGHT(list_qar[2:],measurement_name)
    list_GMT = flt_tag.get_GMT_list(list_qar[2:],measurement_name)
    if max(list_RADIO_HEIGHT) < 10 :
        FLT_status = 'GROUND'
    else:
        FLT_status = 'FLIGHT'

    dic_tag = {
              'AC':ac_id,
              'AC_sector':AC_sector,
               'FLT_number': FLT_number,
               'FLT_status':FLT_status,
                'update_date': update_date,
               'update_time':update_time
                }
    print dic_tag

    # 建立索引表
    put_data_to_index(dic_tag)
    dbname = "CKG_QAR"
    str_IP_address = LOCAL().server_ip()
    user = ''
    password = ''



    print("Create pandas DataFrame:" + file_name)
    start_all_time = time.clock()
    list_no_head = list_qar[2:]
    list_index = range(1,(len(list_qar) - 2 +1),1)#从1开始列号自增的索引
    list_put = list_no_head
    df = pd.DataFrame(data=list_put,
                      index=pd.date_range(start=sector_number,
                                          periods=len(list_put), freq='S'),
                        columns=list_qar[0],
                        dtype='object')
    df['index'] = pd.Series(list_index, index = df.index)
    df['$GMT TIME'] = pd.Series(list_GMT, index = df.index)
    row_number = len(list_no_head)
    print "row_all_number : %s"  % row_number
    div_number = 200
    cut_number = (row_number//div_number) + 1
    last_number = (row_number)%div_number

    #cut_number = 1
    print u"分割数： %s" % cut_number
    list_cut = div_list(list_no_head, cut_number)
    start_write_time = time.time()
    p = Pool()
    for i in range(cut_number):
        start_num = 0 + i * 200
        end_num = 0 + 200 + i * 200
        if i == (cut_number -1):
            end_num = 0 + i * 200 + last_number
        '''
        #print "Write DataFrame  %s " % i
        client.write_points(df[start_num:end_num],
                            measurement = measurement_name,
                            tags= dic_tag)
        '''
        #threading_put_data(df[start_num:end_num],measurement_name,dic_tag)
        p.apply_async(threading_put_data, args=(df[start_num:end_num],measurement_name,dic_tag))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
    end_write_time = time.time()
    wirte_time = end_write_time - start_write_time
    print "write time: %s" % wirte_time
    print "one seconds write : %s  lines" % (row_number/wirte_time)
    end_all_time = time.clock()
    #print "all time: %s" % (end_all_time - start_all_time)
    return row_number, wirte_time

def threading_put_data(df, measurement_name, tags_dict):
    dbname = "CKG_QAR"
    str_IP_address = LOCAL().server_ip()
    user = ''
    password = ''
    client = DataFrameClient(str_IP_address, 8086, user, password, dbname)
    client.write_points(df,
                        measurement = measurement_name,
                        tags= tags_dict)

def put_data_to_index(dict_tag):
    dbname = "DB_sector_index"
    str_IP_address = LOCAL().server_ip()
    user = ''
    password = ''
    client = InfluxDBClient(str_IP_address, 8086, user, password, dbname)
    json_body = [{
        "measurement": "index",
        "tags":dict_tag,
        "fields":dict_tag
    }]
    client.write_points(json_body)


class PUT_DATA():
    def put(self):
        #delete_all_table.delete_all_database()
        #delete_all_table.create_database()
        computer_name = socket.getfqdn(socket.gethostname())
        if computer_name in ["wxjd-61222177.cq.airchina.com.cn", "HUGE"]:
            #单位电脑路径
            dir_path = r'G:\QAR_DATA\append_upload'
        else:
            #服务器电脑路径
            dir_path = '/opt/QAR_DATA/append_upload'

        if os.listdir(dir_path):
            print u"工程部数据有更新，开始译码"
            decode_list = MERGE_DECODE_LIST()
            decode_list.all_decode_list(dir_path, put_data_to_influxDB)
