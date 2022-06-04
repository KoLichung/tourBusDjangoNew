from calendar import month
from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse
import requests
from tourBusCore.models import User ,Order
import urllib 
from django.db.models import Sum
from datetime import datetime, timedelta

# Create your views here.

def base(request):
    return render(request, 'backboard/base.html')

def orders(request):
    q = request.GET.get('order_state')

    orders = Order.objects.all()
    if q!= None:
        orders = orders.filter(state=q)
 
    return render(request, 'backboard/orders.html',{'orders':orders, 'q':q})

def order_detail(request):
    order_id=request.GET.get('order_id')
    theOrder = Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        state = request.POST.get('state')
        theOrder.state = state
        theOrder.save()
        return redirect(f'/backboard/order_detail?order_id={order_id}')

    return render(request, 'backboard/order_detail.html',{'order':theOrder})


