from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tourBusCore.models import User, TourBus, TourBusImage, TourBusRentDay, Order, AnnounceMent,City, County, SmsVerifyCode
from tourBusApi import serializers
from django.db.models import Q
from datetime import datetime
from django.utils.timezone import make_aware
from fcm_django.models import FCMDevice

class BusViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = TourBus.objects.all()
    serializer_class = serializers.TourBusSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user).order_by('-id')
        for i in range(len(queryset)):
            if TourBusImage.objects.filter(tourBus=queryset[i]).count() != 0:
                queryset[i].coverImage = TourBusImage.objects.filter(tourBus=queryset[i]).first().image
            if TourBusRentDay.objects.filter(tourBus=queryset[i]).filter(Q(state="ordered") | Q(state="pasted")).count()!=0:
                recentDay = TourBusRentDay.objects.filter(tourBus=queryset[i]).filter(Q(state="ordered") | Q(state="pasted")).last()
                queryset[i].recent_start_date = recentDay.startDate
                queryset[i].recent_end_date = recentDay.endDate
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TourBusImageViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin):

    queryset = TourBusImage.objects.all()
    serializer_class = serializers.TourBusImageSerializer

    def get_queryset(self):
        if self.request.query_params.get('bus_id')!=None:
            bus_id = self.request.query_params.get('bus_id')
            return self.queryset.filter(tourBus=bus_id)
        else:
            return self.queryset

class OrderViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, state='waitOwnerCheck')

class RentDayViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = TourBusRentDay.objects.all()
    serializer_class = serializers.TourBusRentDaySerializer

    def get_queryset(self):
        if self.request.query_params.get('bus_id') != None:
            bus_id = self.request.query_params.get('bus_id')
            return self.queryset.filter(tourBus=TourBus.objects.get(id=bus_id))
        else:
            return self.queryset

class SearchBusViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,):
    queryset = TourBus.objects.all()
    serializer_class = serializers.TourBusSerializer

    def get_queryset(self):
        fromCityId = self.request.query_params.get('departure_city_id')
        toCityId = self.request.query_params.get('destination_city_id')
        startDate = make_aware(datetime.strptime(self.request.query_params.get('startDate'), '%Y%m%d'))
        endDate = make_aware(datetime.strptime(self.request.query_params.get('endtDate'), '%Y%m%d'))
        numberOfPeople = int(self.request.query_params.get('numberOfPeople'))
        
        theBusses = []
        new_queryset = self.queryset.filter(isTop=True)
        for i in range(len(new_queryset)):
            if TourBusImage.objects.filter(tourBus=new_queryset[i]).count() != 0:
                new_queryset[i].coverImage = TourBusImage.objects.filter(tourBus=new_queryset[i]).first().image
            theBusses.append(new_queryset[i])

        queryset = self.queryset.filter(isTop=False).filter(vehicalSeats__gte=numberOfPeople).filter(city=City.objects.get(id=fromCityId))
        for i in range(len(queryset)):

            if TourBusImage.objects.filter(tourBus=queryset[i]).count() != 0:
                queryset[i].coverImage = TourBusImage.objects.filter(tourBus=queryset[i]).first().image

            rentDays = TourBusRentDay.objects.filter(tourBus=queryset[i], state='available')
            for day in rentDays:
                if startDate >= day.startDate and endDate <= day.endDate:
                    theBusses.append(queryset[i])
            
        return theBusses

class CityViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,):
    queryset = City.objects.all()
    serializer_class = serializers.CitySerializer

class CountyViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,):
    queryset = County.objects.all()
    serializer_class = serializers.CountySerializer

class SmsVerifyViewSet(APIView):

    def get(self, request, format=None):
        from tourBusApi.tasks.smsTasks import randSmsVerifyCode
        phone= self.request.query_params.get('phone')
        if phone!= None and len(phone) == 10:
            # if SmsVerifyCode.objects.filter(phone=phone, is_expired=False).count() ==0:
                code = randSmsVerifyCode(phone)
                return Response({'message': "ok", 'code': code})
            # else:
                # return Response({'message': "this phone already got verify code, try later"})
        else:
            return Response({'message': "wrong phone number type"})

class AnnouncementViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)

    queryset = AnnounceMent.objects.all()
    serializer_class = serializers.AnnouncementSerializer

    def get_queryset(self):
        return self.queryset.order_by('-id')[:10]

    def perform_create(self, serializer):
        # user = serializer.validated_data['user']
        from tourBusApi.tasks.fcmTasks import sendFcmInquiry
        sendFcmInquiry()

        user = self.request.user
        serializer.save(user=user, phone=user.phone, name=user.name)

        

class FCMDeviceViewSet(APIView):

    def post(self, request, format=None):
        #name, active
        try:  
            user_id = request.data.get('user_id')
            registration_id = request.data.get('registration_id')
            device_id = request.data.get('device_id')
            type = request.data.get('type')

            if FCMDevice.objects.filter(device_id=device_id).count() == 0:
                fcmDevice = FCMDevice()
                fcmDevice.user = User.objects.get(id=user_id)
                fcmDevice.registration_id = registration_id
                fcmDevice.device_id = device_id
                fcmDevice.type = type
                fcmDevice.save()
                return Response({'message': "ok"})
            else:
                return Response({'message': "already regist fcm device"})
        except:
            return Response({'message': "error"})

