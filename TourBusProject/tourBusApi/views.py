
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tourBusCore.models import User, TourBus, TourBusImage, TourBusRentDay, Order, AnnounceMent,City, County, SmsVerifyCode
from tourBusApi import serializers

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
        return self.queryset.filter(user=self.request.user)
    
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
        return self.queryset.filter(user=self.request.user)

class RentDayViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,):
    queryset = TourBusRentDay.objects.all()
    serializer_class = serializers.TourBusRentDaySerializer

    def get_queryset(self):
        bus_id = self.request.query_params.get('bus_id')
        return self.queryset.filter(tourBus=TourBus.objects.get(id=bus_id))

class SearchBusViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,):
    queryset = TourBus.objects.all()
    serializer_class = serializers.TourBusSerializer

    def get_queryset(self):
        return self.queryset

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
            if SmsVerifyCode.objects.filter(phone=phone, is_expired=False).count() ==0:
                code = randSmsVerifyCode(phone)
                return Response({'message': "ok", 'code': code})
            else:
                return Response({'message': "this phone already got verify code, try later"})
        else:
            return Response({'message': "wrong phone number type"})


