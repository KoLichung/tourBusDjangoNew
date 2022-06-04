from django.urls import path, include
from . import views
from django.shortcuts import render
from django.http import HttpResponse 
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('base', views.base, name = 'base'), 
    path('order_detail', views.order_detail, name='order_detail'), 
    path('orders', views.orders, name='orders'), 
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout')
]