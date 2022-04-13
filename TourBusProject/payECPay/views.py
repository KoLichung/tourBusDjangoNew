from rest_framework.views import APIView
from rest_framework.response import Response
from .aesCipher import AESCipher

import requests
import json
import time
import urllib.parse
import logging

logger = logging.getLogger(__file__)

class GetTokenView(APIView):

    def get(self, request, format=None):
        post_url = 'https://ecpg-stage.ecpay.com.tw/Merchant/GetTokenbyTrade'
        timeStamp = int( time.time() )

        data = {
                "MerchantID": "3002607",
                "RememberCard": 0,
                "PaymentUIType": 2,
                "ChoosePaymentList": "1,3",
                "OrderInfo": {
                    "MerchantTradeNo": "J202203170903",
                    "MerchantTradeDate": "2022/03/17 09:03:12",
                    "TotalAmount": 100,
                    "ReturnURL": "https://yourReturnURL.com",
                    "TradeDesc": "item description",
                    "ItemName": "item1#item2"
                },
                "CardInfo": {
                    "OrderResultURL": "https://yourOrderResultURL.com",
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
                }
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
        print(body)

        logger.info(body)

        # content = body['content']
        # print(content)

        return Response("1|OK")