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
        fields = ('id', 'user', 'title', 'lat', 'lng', 'city', 'county', 'vehicalSeats','vehicalLicence','vehicalOwner','vehicalLicenceImage', 'driverLicenceImage', 'vehicalYearOfManufacture','isPublish','isTop','coverImage', 'recent_start_date', 'recent_end_date')
        read_only_fields = ('id','user','isTop')

class TourBusImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBusImage
        fields = '__all__'
        read_only_fields = ('id',)

class OrderSerializer(serializers.ModelSerializer):
    busTitle = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    coverImage = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'tourBus', 'state', 'startDate', 'endDate', 'depatureCity', 'destinationCity', 'orderMoney', 'depositMoney', 'busTitle', 'name', 'phone', 'memo', 'coverImage', 'isAtm', 'ATMInfoBankCode', 'ATMInfovAccount', 'ATMInfoExpireDate')
        read_only_fields = ('id','user', 'busTitle', 'name', 'phone')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['busTitle'] =  instance.tourBus.title
        rep['name'] = instance.user.name
        rep['phone'] = instance.user.phone
        return rep

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['tourBus'] =  TourBusSerializer(instance.tourBus).data
    #     return rep

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

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnounceMent
        fields = '__all__'
        read_only_fields = ('id','user','phone', 'name')