import json

import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from shopowner.models import UserAccounts, MpesaReceipts
from shopowner.mpesa_integration.mpesa_api import MpesaApi

mpesaClient=MpesaApi()
class Home(TemplateView):
    template_name = 'index.html'

def createCustomerAccount(request):
    message = {}
    if request.method == 'POST':
        f_name=request.POST['fname']
        l_name = request.POST['lname']
        e_address = request.POST['email']
        username = request.POST['uname']
        password = request.POST['passwd']
        c_pass = request.POST['cpass']

        if password !=c_pass:
            message['error']="Password do not match"
        else:
            user=UserAccounts.objects.create_user(first_name=f_name,last_name=l_name,email=e_address,username=username,password=password)
            message['success']="Account Successfully created"

    return render(request,'signup.html',{'message':message})
def lipanaMpesaOnline(request):
    if request.method == 'POST':
        mobile_phone=request.POST['phone']
        amount_payed = request.POST['amount']
        url_endpoint = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % mpesaClient.generateMpesaAccessToken()}
        options = {
            "BusinessShortCode": "174379",
            "Password": mpesaClient.generateLipanaMpesaPassword(),
            "Timestamp": mpesaClient.lipaTime,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",
            "PartyA": "254115224758",
            "PartyB": "174379",
            "PhoneNumber": "254115224758",
            "CallBackURL": "https://5c5f-197-156-137-147.ngrok.io/confirmation/",
            "AccountReference": "Test",
            "TransactionDesc": "Test"
        }
        response = requests.post(url_endpoint, json=options, headers=headers)
        return HttpResponse("success")
    else:
        return render(request,'lipa.html')

@csrf_exempt
def mpesaConfirmation(request):
    print("The confirmation has been hit")
    mpesa_response_body=request.body
    mpesa_payment_response=json.loads(mpesa_response_body)
    print(mpesa_payment_response)
    amount=mpesa_payment_response['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    mpesaReceiptNumber = mpesa_payment_response['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    transactionDate = mpesa_payment_response['Body']['stkCallback']['CallbackMetadata']['Item'][2]['Value']
    phoneNumber = mpesa_payment_response['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    MpesaReceipts.objects.create(amount=amount,mpesaReceiptNumber=mpesaReceiptNumber,transactionDate=transactionDate,phoneNumber=phoneNumber)