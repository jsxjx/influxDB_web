#coding=utf-8

from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from IP_judge import LOCAL

def add_sign(string1):
    string2 ="\"" + str(string1) + "\""
    return string2

def add_single_quotes(string1):
    string2 = "'" + str(string1) + "'"
    return string2

def merge_str(str1, str2):
    result = str1 + "," + str2
    return result

class influxDB_interface():

    def __init__(self):
        pass

    def DFclient(self, dbname):
        str_IP_address = LOCAL().server_ip()
        user = ''
        password = ''
        clientdb = DataFrameClient(str_IP_address, 8086, user, password, dbname)
        return clientdb

    def inf_query(self, dbname, value, mes):
        sql_str = "SELECT " + value + " FROM " + mes
        result = self.DFclient(dbname).query(sql_str)
        return result

    def list_query(self, dbname, list, mes, AC_sector):
        index_str = add_sign('index') + ","
        value_str = reduce(merge_str, map(add_sign, list))
        mes_str = add_sign(mes)
        where_str = " WHERE \"AC_sector\" =" + add_single_quotes(AC_sector)
        print value_str
        sql_str = "SELECT " + index_str + value_str + " FROM " + mes_str + where_str
        print sql_str
        result = self.DFclient(dbname).query(sql_str)
        result = result[mes]
        return result

query_result = influxDB_interface().list_query("CKG_QAR",["623:STBY HYD OIL PRESSURE","463:GUIDANCE CUE X POSITION"],'737_7', 'B-1527_20150901023317')
query_result.index = range(1,(len(query_result.index)+1),1)
new_df = query_result.fillna('-')
result_json = new_df.to_dict(orient="records")
print result_json
