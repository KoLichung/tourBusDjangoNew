from rest_framework import serializers
from tourBusCore.models import TourBus, TourBusImage, TourBusRentDay, Order, AnnounceMent,City, County

class TourBusSerializer(serializers.ModelSerializer):
    # coverImage = serializers.ImageField(max_length=None, allow_empty_file=True)
    # CategoryNum = serializers.IntegerField(default='0')
    coverImage = serializers.CharField(read_only=True)
    recent_start_date = serializers.DateTimeField(read_only=True)
    recent_end_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TourBus
        fields = ('id', 'user', 'title', 'lat', 'lng', 'city', 'county', 'vehicalSeats','vehicalLicence','vehicalOwner','vehicalEngineNumber','vehicalBodyNumber','vehicalLicenceImage','coverImage', 'recent_start_date', 'recent_end_date')
        read_only_fields = ('id','user')

class TourBusImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBusImage
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