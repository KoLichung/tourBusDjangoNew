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
router.register('tour_bus_images', views.TourBusImageViewSet)
router.register('announcements', views.AnnouncementViewSet)

app_name = 'tourBusApi'

urlpatterns = [
    path('', include(router.urls)),
    path('sms_verify', views.SmsVerifyViewSet.as_view()),
    path('device_register', views.FCMDeviceViewSet.as_view()),
    path('owner_orders', views.OwnerBussesOrdersViewSet.as_view()),
    path('owner_update_state', views.OwnerUpdateOrderStateViewSet.as_view()),
    path('owner_update_memo', views.OwnerUpdateOrderMemoViewSet.as_view()),
    path('get_order_image', views.GetOrderImageViewSet.as_view()),
    path('get_order_user_info', views.GetOrderUserInfo.as_view()),
    path('reset_password_sms_verify', views.ResetPasswordSmsVerifyViewSet.as_view()),
    path('reset_password_sms_password', views.ResetPasswordSmsSendPasswordViewSet.as_view()),
]
