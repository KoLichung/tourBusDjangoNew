from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tourBusApi import views

router = DefaultRouter()
router.register('busses', views.BusViewSet)
router.register('orders', views.OrderViewSet)
router.register('bus_rent_days', views.RentDayViewSet)
router.register('search_bus', views.SearchBusViewSet)
router.register('cities', views.CityViewSet)
router.register('counties', views.CountyViewSet)

app_name = 'tourBusApi'

urlpatterns = [
    path('', include(router.urls)),
    path('sms_verify', views.SmsVerifyViewSet.as_view()),
]