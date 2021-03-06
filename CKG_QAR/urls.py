# coding:utf-8
"""CKG_QAR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #主页，首页
    url(r'^$', 'main_web.views.home', name='home'),
    url(r'^home/$', 'main_web.views.home', name='home'),
    #查询页面
    url(r'^all_childtable_index_list/$','main_web.views_query.all_childtable_index_list',
        name = 'all_childtable_index_list'),
    url(r'^childtable/(.+)/$', 'main_web.views_query.childtable', name = 'childtable'),
    url(r'^runup_list/$', 'main_web.views_query.runup_list'),
    url(r'^query_index/$', 'main_web.views_query.query_index'),
    # 参数查询ajxa 模块
    url(r'^ajax_some_para/$', 'main_web.views_query.ajax_some_para',
        name = 'ajax_some_para'),
    # 模版存储
    url(r'^storing_stencil/$', 'main_web.views_stencil.storing_stencil'),
    url(r'^storing_stencil_ajax/$',
        'main_web.views_stencil.storing_stencil_ajax',
        name = 'storing_stencil_ajax'),
    #模版编辑，添加图表
    url(r'^stencil_list/$', 'main_web.views_stencil.stencil_list'),
    url(r'^edit_stencil/(.+)/$', 'main_web.views_stencil.edit_stencil', name = 'edit_stencil'),
    url(r'^stencil_echarts/$', 'main_web.views_stencil.stencil_echarts', name = 'stencil_echarts'),
    #趋势
    url(r'^tendency_total/$', 'main_web.views_query.tendency_total'),
    url(r'^tendency_single/$', 'main_web.views_query.tendency_single'),
    url(r'^tendency_single_para_list', 'main_web.views_query.tendency_single_para_list', name = 'tendency_single_para_list'),
    #eFlow趋势统计
    url(r'^eFlow_total/$', 'main_web.views_query.eFlow_total'),
    #使用说明
    url(r'^guide/$', 'main_web.views.guide'),
]
