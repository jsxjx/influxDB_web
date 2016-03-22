#coding=utf-8

from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from IP_judge import LOCAL

def to_str(str1, str2):
    result = str1 + ", " + str2
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

    def list_query(self, dbname, list, mes):
        value_str = reduce(to_str, list)
        sql_str = "SELECT " + value_str + " FROM " + mes
        result = self.DFclient(dbname).query(sql_str)
        return result


