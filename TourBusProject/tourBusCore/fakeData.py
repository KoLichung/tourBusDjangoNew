import csv
import os
from datetime import datetime, timedelta
from .models import User, TourBus, TourBusImage, TourBusRentDay, Order, AnnounceMent,City, County


def importCityCounty():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'county.csv')

    file = open(file_path)
    reader = csv.reader(file, delimiter=',')
    for index, row in enumerate(reader):
        if index != 0:
            if City.objects.filter(name=row[0]).count()==0:
                city = City()
                city.name = row[0]
                city.lat = row[3]
                city.lng = row[4]
                city.save()
            else:
                city = City.objects.get(name=row[0])

            county_name = row[2].replace(row[0],'')
            if County.objects.filter(name=county_name).count()==0:
                county = County()
                county.city = city
                county.name = county_name
                county.lat = row[3]
                county.lng = row[4]
                county.save()

def fakeData():
    user = User()
    user.name = 'testUser'
    user.phone = '0989123456'
    user.isOwner = False
    user.save()

    user = User()
    user.name = 'testOwner'
    user.phone = '0945123456'
    user.isOwner = True
    user.company = 'test company'
    user.address = 'test address'
    user.vehicalLicence = 'test licence'
    user.vehicalOwner = 'test owner'
    user.vehicalEngineNumber = 'test engine number'
    user.vehicalBodyNumber = 'test body number'
    user.save()

    user = User.objects.all()[0]

    tourBus = TourBus()
    tourBus.user = user
    tourBus.title = 'test title'
    tourBus.city = City.objects.all()[0]
    tourBus.county = County.objects.filter(city=tourBus.city)[0]
    tourBus.lat = tourBus.county.lat
    tourBus.lng = tourBus.county.lng
    tourBus.vehicalSeats = 30
    tourBus.vehicalLicence = 'test licence'
    tourBus.vehicalOwner = 'test owner'
    tourBus.vehicalEngineNumber = 'test engine number'
    tourBus.vehicalBodyNumber = 'test body number'
    tourBus.isPublish = True
    tourBus.save()

    tourBusRentDay = TourBusRentDay()
    tourBusRentDay.tourBus = tourBus
    tourBusRentDay.state = 'avaliable'
    tourBusRentDay.startDate = datetime.now()
    tourBusRentDay.endDate = tourBusRentDay.startDate + timedelta(days=2)
    tourBusRentDay.save()

    order = Order()
    order.user = user
    order.tourBus = tourBus
    order.state =  'waitOwnerCheck'
    order.startDate = datetime.now() + timedelta(days=1)
    order.endDate = datetime.now() + timedelta(days=3)
    order.depatureCity = City.objects.all()[2]
    order.destinationCity = City.objects.all()[3]
    order.save()

    tourBus = TourBus()
    tourBus.user = user
    tourBus.title = 'test title'
    tourBus.city = City.objects.all()[2]
    tourBus.county = County.objects.filter(city=tourBus.city)[2]
    tourBus.lat = tourBus.county.lat
    tourBus.lng = tourBus.county.lng
    tourBus.vehicalSeats = 30
    tourBus.vehicalLicence = 'test licence 2'
    tourBus.vehicalOwner = 'test owner 2'
    tourBus.vehicalEngineNumber = 'test engine number 2'
    tourBus.vehicalBodyNumber = 'test body number 2'
    tourBus.isPublish = True
    tourBus.save()

    tourBusRentDay = TourBusRentDay()
    tourBusRentDay.tourBus = tourBus
    tourBusRentDay.state = 'avaliable'
    tourBusRentDay.startDate = datetime.now() + timedelta(days=1)
    tourBusRentDay.endDate = tourBusRentDay.startDate + timedelta(days=3)
    tourBusRentDay.save()
    
    order = Order()
    order.user = user
    order.tourBus = tourBus
    order.state =  'waitOwnerCheck'
    order.startDate = datetime.now() + timedelta(days=1)
    order.endDate = datetime.now() + timedelta(days=3)
    order.depatureCity = City.objects.all()[2]
    order.destinationCity = City.objects.all()[3]
    order.save()

    announcement = AnnounceMent()
    announcement.user = user
    announcement.announceDateTime = datetime.now()
    announcement.numbersOfPeople = 25
    announcement.startDateTime = datetime.now() + timedelta(days=1)
    announcement.endDateTime = datetime.now() + timedelta(days=3)
    announcement.depatureCity = City.objects.all()[0]
    announcement.destinationCity = City.objects.all()[2]
    announcement.memo = 'this is memo'
    announcement.save()

