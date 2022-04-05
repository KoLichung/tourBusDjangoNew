from django.contrib import admin
from .models import User, TourBus, TourBusImage, TourBusRentDay, Order, AnnounceMent, City, County
from .models import SmsVerifyCode

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'line_id')

@admin.register(TourBus)
class TourBusAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'title', 'city', 'county')

@admin.register(TourBusImage)
class TourBusImageAdmin(admin.ModelAdmin):
    list_display = ('id','tourBus', 'type', 'image')

@admin.register(TourBusRentDay)
class TourBusRentDayAdmin(admin.ModelAdmin):
    list_display = ('id','tourBus', 'state', 'startDate', 'endDate')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'tourBus', 'startDate', 'endDate')

@admin.register(AnnounceMent)
class AnnounceMentAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'announceDateTime', 'startDateTime', 'depatureCity', 'destinationCity')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'lat', 'lng')

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'city', 'lat', 'lng')

@admin.register(SmsVerifyCode)
class SmsVerifyCodeAdmin(admin.ModelAdmin):
    list_display = ('id','phone', 'code', 'is_expired')