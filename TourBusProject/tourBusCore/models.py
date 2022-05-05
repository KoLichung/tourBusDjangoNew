from email.policy import default
import pathlib
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse

class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not phone:
            raise ValueError('Users must have an phone')
        # user = self.model(email=self.normalize_email(email), **extra_fields)
        user = self.model(
            phone = phone, 
            name=extra_fields.get('name'),
            line_id=extra_fields.get('line_id'),
            isOwner=extra_fields.get('isOwner'),
            company=extra_fields.get('company'),
            address=extra_fields.get('address'),
            vehicalLicence=extra_fields.get('vehicalLicence'),
            vehicalOwner=extra_fields.get('vehicalOwner'),
            # vehicalEngineNumber=extra_fields.get('vehicalEngineNumber'),
            # vehicalBodyNumber=extra_fields.get('vehicalBodyNumber'),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password, **extra_fields):
        """Creates and saves a new super user"""
        user = self.create_user(phone, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


def image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) #uuid1 -> uuid + timestamp
    return f'images/{new_fname}{fpath.suffix}'

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    phone = models.CharField(max_length=10, unique=True, blank = True, null=True)
    name = models.CharField(max_length=255, blank = True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    isOwner = models.BooleanField(default=False, blank = True, null=True)
    isPassed = models.BooleanField(default=False, blank = True, null=True)
    company = models.CharField(max_length=255, default='', blank = True, null=True)
    address = models.CharField(max_length=255, default='', blank = True, null=True)
    vehicalLicence = models.CharField(max_length=255, default='', blank = True, null=True)
    vehicalOwner = models.CharField(max_length=255, default='', blank = True, null=True)
    # vehicalEngineNumber = models.CharField(max_length=255, default='', blank = True, null=True)
    # vehicalBodyNumber = models.CharField(max_length=255, default='', blank = True, null=True)

    driverLicenceImage = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)
    vehicalLicenceImage = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

    line_id = models.CharField(max_length=255, default='', blank = True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

class TourBus(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, default='', blank = True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    city = models.CharField(max_length=100, default='', blank = True, null=True)
    county = models.CharField(max_length=100, default='', blank = True, null=True)

    vehicalSeats = models.IntegerField(default=0, null=True)
    vehicalLicence = models.CharField(max_length=255, default='', blank = True, null=True)
    vehicalOwner = models.CharField(max_length=255, default='', blank = True, null=True)
    # vehicalEngineNumber = models.CharField(max_length=255, default='', blank = True, null=True)
    # vehicalBodyNumber = models.CharField(max_length=255, default='', blank = True, null=True)
    driverLicenceImage = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)
    vehicalLicenceImage = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)
    vehicalYearOfManufacture = models.CharField(max_length=20, default='', blank = True, null=True)

    isPublish = models.BooleanField(default=False, null=True)
    isTop = models.BooleanField(default=False, null=True)

class TourBusImage(models.Model):
    tourBus = models.ForeignKey(
        TourBus,
        on_delete=models.CASCADE
    )

    # exterior, interior, luggage
    type = models.CharField(max_length=100, default='', blank = True, null=True)
    image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

class TourBusRentDay(models.Model):
    tourBus = models.ForeignKey(
        TourBus,
        on_delete=models.CASCADE
    )

    # available, ordered, pasted
    state = models.CharField(max_length=100, default='', blank = True, null=True)
    startDate = models.DateTimeField(auto_now=False,null=True)
    endDate = models.DateTimeField(auto_now=False,null=True)

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT
    )

    tourBus = models.ForeignKey(
        TourBus,
        on_delete=models.RESTRICT
    )

    # waitOwnerCheck, ownerCanceled, waitForDeposit, waitForAtmDeposit
    # ownerWillContact, onTheWay, closed
    state =  models.CharField(max_length=100, default='', blank = True, null=True)

    startDate = models.DateTimeField(auto_now=False,null=True)
    endDate = models.DateTimeField(auto_now=False,null=True)

    depatureCity = models.CharField(max_length=100, default='', blank = True, null=True)
    destinationCity = models.CharField(max_length=100, default='', blank = True, null=True)

    orderMoney = models.IntegerField(default=0, null=True)
    depositMoney = models.IntegerField(default=0, null=True)

    memo = models.TextField(default='', null=True, blank=True)

    isAtm = models.BooleanField(default=False, blank = True, null=True)
    ATMInfoBankCode = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfovAccount = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfoExpireDate = models.DateTimeField(auto_now=False, blank = True,null=True)

class PayInfo(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT
    )
    
    PaymentType = models.CharField(max_length=100, default='', blank = True, null=True)
    MerchantID = models.CharField(max_length=100, default='', blank = True, null=True)
    
    OrderInfoMerchantTradeNo = models.CharField(max_length=100, default='', blank = True, null=True)
    OrderInfoTradeDate = models.DateTimeField(auto_now=False,null=True)
    OrderInfoTradeNo = models.CharField(max_length=100, default='', blank = True, null=True)
    OrderInfoTradeAmt = models.IntegerField(default=0, null=True)
    OrderInfoPaymentType = models.CharField(max_length=20, default='', blank = True, null=True)
    OrderInfoChargeFee = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    OrderInfoTradeStatus = models.CharField(max_length=20, default='', blank = True, null=True)

    ATMInfoBankCode = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfovAccount = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfoExpireDate = models.DateTimeField(auto_now=False,null=True)

    CardInfoAuthCode = models.CharField(max_length=100, default='', blank = True, null=True)
    CardInfoGwsr = models.IntegerField(default=0, null=True)
    CardInfoProcessDate =  models.DateTimeField(auto_now=False,null=True)
    CardInfoAmount = models.IntegerField(default=0, null=True)
    CardInfoCard6No = models.CharField(max_length=20, default='', blank = True, null=True)
    CardInfoCard4No = models.CharField(max_length=20, default='', blank = True, null=True)


class AnnounceMent(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=10, blank = True, null=True)
    name = models.CharField(max_length=255, blank = True, null=True)

    announceDateTime = models.DateTimeField(auto_now=False,null=True)
    numbersOfPeople = models.IntegerField(default=0)
    startDateTime = models.DateTimeField(auto_now=False,null=True)
    endDateTime = models.DateTimeField(auto_now=False,null=True)
    depatureCity = models.CharField(max_length=100, default='', blank = True, null=True)
    destinationCity = models.CharField(max_length=100, default='', blank = True, null=True)
    memo = models.TextField(default='')

class City(models.Model):
    name = models.CharField(max_length=100, default='', blank = True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

class County(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, default='', blank = True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

class SmsVerifyCode(models.Model):
    phone = models.CharField(max_length=10)
    code = models.CharField(max_length=4)
    is_expired = models.BooleanField(default=False)