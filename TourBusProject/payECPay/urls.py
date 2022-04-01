from django.urls import path

from payECPay import views

app_name = 'stockBackTest'

urlpatterns = [
    path('get_token', views.GetTokenView.as_view()),
]