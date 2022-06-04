from calendar import month
from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse
import requests
from tourBusCore.models import User ,Order
from django.contrib import auth
from django.contrib.auth import authenticate, logout
# Create your views here.

def base(request):
    return render(request, 'backboard/base.html')

def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/backboard/orders')
        else:
            return redirect('/backboard/')

    return render(request, 'backboard/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/backboard/')

def orders(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    q = request.GET.get('order_state')
    orders = Order.objects.all().order_by('-id')
    if q!= None:
        orders = orders.filter(state=q)
 
    return render(request, 'backboard/orders.html',{'orders':orders, 'q':q})

def order_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    order_id=request.GET.get('order_id')
    theOrder = Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        state = request.POST.get('state')
        theOrder.state = state
        theOrder.save()
        return redirect(f'/backboard/order_detail?order_id={order_id}')

    return render(request, 'backboard/order_detail.html',{'order':theOrder})


