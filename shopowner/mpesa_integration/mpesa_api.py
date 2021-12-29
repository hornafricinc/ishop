import base64
from datetime import datetime
import json

import requests
from requests.auth import HTTPBasicAuth


class MpesaApi:
    businessShortCodeLipaOnline="174379"
    lipaTime=datetime.now().strftime("%Y%m%d%H%M%S")


    def generateMpesaAccessToken(self):
        consumerKey="nT7qX3lciMt5J96oP1QVoD27VdqWaK8U"
        consumerSecret="i6Hq5LAPbhJhYV4H"
        apiURL="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response=requests.get(apiURL,auth=HTTPBasicAuth(consumerKey,consumerSecret))
        mpesa_access_token_content=json.loads(response.text)
        generated_access_token=mpesa_access_token_content['access_token']
        return generated_access_token
    def generateLipanaMpesaPassword(self):
        passKey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        data_to_encode=self.businessShortCodeLipaOnline+passKey+self.lipaTime
        encoded_data=base64.b64encode(data_to_encode.encode())
        decoded_online_password=encoded_data.decode('utf-8')
        return decoded_online_password
    def lipanaMpesaOnline(self,amount,paying_phone):
        apiURL="https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers={"Authorization":"Bearer %s" % self.generateMpesaAccessToken()}
        request_body={
                   "BusinessShortCode":self.businessShortCodeLipaOnline,
                   "Password": self.generateLipanaMpesaPassword(),
                   "Timestamp":self.lipaTime,
                   "TransactionType": "CustomerPayBillOnline",
                   "Amount":amount,
                   "PartyA":paying_phone,
                   "PartyB":self.businessShortCodeLipaOnline,
                   "PhoneNumber":paying_phone,
                   "CallBackURL":" https://3401-102-166-95-11.ngrok.io/confirmation",
                   "AccountReference":"Test Account",
                    "TransactionDesc":"Test Account"
                }
        response=requests.post(apiURL,json=request_body,headers=headers)
        return response
