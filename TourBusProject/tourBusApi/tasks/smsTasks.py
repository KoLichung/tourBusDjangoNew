from celery import shared_task
import requests
from tourBusCore.models import SmsVerifyCode
import math, random

def testSMS():
    print('test mitake sms')
    url = 'https://smsb2c.mitake.com.tw/b2c/mtk/SmSend?CharsetURL=UTF8'

    testString = "這個是一個測試 0012"

    params ={
        "username": "0938651226",
        "password": "123456",
        "dstaddr": "0912585506",
        "smbody": testString
    }

    resp = requests.post(url, params= params)

    print(resp.text)

def sendSMSCode(phone, code):
    url = 'https://smsb2c.mitake.com.tw/b2c/mtk/SmSend?CharsetURL=UTF8'

    theString = f"您的驗證碼為 {code}, 請盡快驗證~"
    params ={
        "username": "0938651226",
        "password": "123456",
        "dstaddr": phone,
        "smbody": theString
    }
    resp = requests.post(url, params= params)
    print(resp.text)

def randSmsVerifyCode(phone):
    smsVerifyCode = SmsVerifyCode()
    smsVerifyCode.phone = phone
    smsVerifyCode.code = generateOTP()
    smsVerifyCode.save()
    sendSMSCode(smsVerifyCode.phone, smsVerifyCode.code)
    expireSmsCode.apply_async(kwargs={'id': smsVerifyCode.id}, countdown=60)
    return smsVerifyCode.code

def smsSendPassword(phone, password):
    url = 'https://smsb2c.mitake.com.tw/b2c/mtk/SmSend?CharsetURL=UTF8'

    theString = f"您的臨時密碼為 {password}, 請盡快登入並修改~"
    params ={
        "username": "0938651226",
        "password": "123456",
        "dstaddr": phone,
        "smbody": theString
    }
    resp = requests.post(url, params= params)
    print(resp.text)

def generateOTP() :
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
    # length of password can be changed
    # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    
    # ex.3211
    return OTP

@shared_task
def expireSmsCode(id):
    smsVerifyCode = SmsVerifyCode.objects.get(id=id)
    smsVerifyCode.is_expired = True
    smsVerifyCode.save()
