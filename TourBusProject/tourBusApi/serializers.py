from rest_framework import serializers
from tourBusCore.models import User, TourBus, TourBusImage, TourBusRentDay, Order, AnnounceMent,City, County

class TourBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBus
        fields = '__all__'
        read_only_fields = ('id',)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id',)

class TourBusRentDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBusRentDay
        fields = '__all__'
        read_only_fields = ('id',)

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        read_only_fields = ('id',)

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'
        read_only_fields = ('id',)