# coding:utf-8
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from arrow_time import today_date_for_influxd_sql
from arrow_time import ten_day_ago_for_influxd_sql
from influxdb_function import influxDB_interface


def home(request):
    date_start = today_date_for_influxd_sql()
    date_end = today_date_for_influxd_sql()


    where_str = " WHERE time > " + "'" + date_start + "'" + " - 8h" + " AND time < " + "'" + date_end + "'" + " + 16h"
    infdb_if = influxDB_interface()
    sector_index = infdb_if.inf_query("DB_sector_index", "*", "index", where_str)
    if sector_index <> {}:
        df = sector_index['index']
        result_json = df.to_json(orient="records")
        return render(request, 'home.html', {'result_json': result_json})
    else:

        return render(request, 'home.html', {'result_json': {}})

def guide(request):
    return render(request, 'guide.html')
