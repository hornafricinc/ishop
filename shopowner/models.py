from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserAccounts(AbstractUser):
    is_owner=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=False)

    class Meta:
        db_table='system_users'
class Products(models.Model):
    adding_user=models.ForeignKey(UserAccounts,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=50,blank=False,null=False)
    selling_price=models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        db_table='products'
class MpesaReceipts(models.Model):
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    mpesaReceiptNumber=models.CharField(max_length=10,blank=False)
    transactionDate=models.DateTimeField()
    phoneNumber=models.CharField(max_length=12,blank=False)

    class Meta:
        db_table='mpesareceipts'
