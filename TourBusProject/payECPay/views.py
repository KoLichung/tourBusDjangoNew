from rest_framework.views import APIView
from rest_framework.response import Response
from .aesCipher import AESCipher
from datetime import datetime
from random import randint

import requests
import json
import time
import urllib.parse
import logging

from tourBusCore.models import PayInfo, Order

logger = logging.getLogger(__file__)

def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

class GetTokenView(APIView):

    def get(self, request, format=None):
        post_url = 'https://ecpg-stage.ecpay.com.tw/Merchant/GetTokenbyTrade'
        timeStamp = int( time.time() )

        data = {
                "MerchantID": "1332298",
                "RememberCard": 0,
                "PaymentUIType": 2,
                "ChoosePaymentList": "1,3",
                "OrderInfo": {
                    "MerchantTradeNo": f"J{random_with_N_digits(12)}",
                    "MerchantTradeDate": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    "TotalAmount": 100,
                    "ReturnURL": "http://45.77.25.172/api/ecpay/post_callback",
                    "TradeDesc": "item description",
                    "ItemName": "item1#item2"
                },
                "CardInfo": {
                    "OrderResultURL": "https://www.ecpay.com.tw/",
                    "CreditInstallment": "3,6,9,12"
                },
                "ATMInfo": {
                    "ExpireDate": 3
                },
                "ConsumerInfo": {
                    "MerchantMemberID": "test123456",
                    "Email": "customer@email.com",
                    "Phone": "0912345678",
                    "Name": "Test",
                    "CountryCode": "158"
                },
                "CustomField": "1",
        }
        
        print(str(data).replace(": ",':').replace(", ",',').replace("'",'"'))
        #url encode
        encode_text = urllib.parse.quote(str(data).replace(": ",':').replace(", ",',').replace("'",'"'))

        cipher = AESCipher()
        encrypt_text = cipher.encrypt(encode_text)

        postData = {
            "MerchantID": "3002607",
            "RqHeader": {
                "Timestamp": str(timeStamp),
                "Revision": "1.3.22"
            },
            "Data": encrypt_text
        }

        resp = requests.post(post_url, json = postData)

        respData = json.loads(resp.text)['Data']
        decrypt_text = cipher.decrypt(respData)
        the_data = urllib.parse.unquote(decrypt_text)

        return Response(json.loads(the_data))

class PaymentResultCallback(APIView):

    def post(self, request, format=None):
        # body_unicode = request.body.decode('utf-8')
        body = json.loads(request.body)
        # print(body)
        
        cipher = AESCipher()
        data = body['Data']
        decrypt_text = cipher.decrypt(data)
        the_data = urllib.parse.unquote(decrypt_text)

        data_json = json.loads(the_data)

        if(PayInfo.objects.filter(OrderInfoMerchantTradeNo=data_json['OrderInfo']['MerchantTradeNo']).count()==0 ):
            payInfo = PayInfo()
            payInfo.MerchantID = data_json['MerchantID']

            if(data_json['OrderInfo']!=None):
                payInfo.OrderInfoMerchantTradeNo = data_json['OrderInfo']['MerchantTradeNo']
                payInfo.OrderInfoTradeDate = datetime.strptime(data_json['OrderInfo']['TradeDate'], "%Y/%m/%d %H:%M:%S")  
                payInfo.OrderInfoTradeNo = data_json['OrderInfo']['TradeNo']
                payInfo.OrderInfoTradeAmt = data_json['OrderInfo']['TradeAmt']
                payInfo.OrderInfoPaymentType = data_json['OrderInfo']['PaymentType']
                payInfo.OrderInfoChargeFee = data_json['OrderInfo']['ChargeFee']
                payInfo.OrderInfoTradeStatus = data_json['OrderInfo']['TradeStatus']

            if(data_json['CardInfo']!=None):
                payInfo.PaymentType = "信用卡"
                payInfo.CardInfoAuthCode = data_json['CardInfo']['AuthCode']
                payInfo.CardInfoGwsr = data_json['CardInfo']['Gwsr']
                payInfo.CardInfoProcessDate = datetime.strptime(data_json['CardInfo']['ProcessDate'], "%Y/%m/%d %H:%M:%S")  
                payInfo.CardInfoAmount = data_json['CardInfo']['Amount']
                payInfo.CardInfoCard6No = data_json['CardInfo']['Card6No']
                payInfo.CardInfoCard4No = data_json['CardInfo']['Card4No']
            
            if(data_json['CustomField']!=None):
                payInfo.order = Order.objects.get(id= int(data_json['CustomField']) )
            else:
                payInfo.order = Order.objects.get(id=1)

            payInfo.save()
            
            
        # print(the_data)


        logger.info(body)
        logger.info(data_json)

        # content = body['content']
        # print(content)

        return Response("1|OK")

    