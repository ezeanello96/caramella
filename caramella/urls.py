# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from helados import settings
import views

urlpatterns = [
    url(r'^$', views.index, name='inicio'),
    url(r'^cargarLatas/', views.cargarLatas, name='cargarLatas'),
    url(r'^remito/', views.remito, name='remito'),
    url(r'^verStock/', views.verStock, name='verStock'),
    url(r'^clientes/', views.clientes, name='clientes'),
    url(r'^ventas/', views.stats, name='stats'),
]