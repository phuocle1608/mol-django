from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
import datetime

# Create your models here.
class Source(models.Model):
    Source_Id = models.AutoField(primary_key=True)
    Source_Name = models.CharField(max_length=255)
    Source_Link = models.CharField(max_length=255)

    def __str__(self):
        return self.Source_Name


class Product(models.Model):
    Product_Id = models.AutoField(primary_key = True)
    Product_Name = models.CharField(max_length=255)
    Product_Price = models.BigIntegerField()
    IsActive = models.IntegerField()

    def __str__(self):
        return self.Product_Name


class Customer(models.Model):
    Customer_Id = models.AutoField(primary_key=True)
    Customer_Name = models.CharField(max_length=255)
    Customer_Facebook = models.CharField(max_length=255)
    Customer_Phone = models.CharField(max_length=10, null=True)
    Customer_ZaloName = models.CharField(max_length=255, null=True)
    Customer_Address = models.CharField(max_length=255, null=True)
    Source_Id = models.ForeignKey(Source, on_delete=models.CASCADE, db_column='Source_Id')

    def __str__(self):
        return self.Customer_Name

class Workingstatus(models.Model):
    Workingstatus_Id = models.AutoField(primary_key=True)
    Workingstatus_Name = models.CharField(max_length=50)

    def __str__(self):
        return self.Workingstatus_Name

class Paymentstatus(models.Model):
    Paymentstatus_Id = models.AutoField(primary_key=True)
    Paymentstatus_Name = models.CharField(max_length=50)

    def __str__(self):
        return self.Paymentstatus_Name

class Donhang(models.Model):
    Donhang_Id = models.AutoField(primary_key=True)
    Donhang_Name = models.CharField(max_length=255)
    FlashDesign_Flag = models.IntegerField()
    Workingstatus_Id = models.ForeignKey(Workingstatus, on_delete=models.CASCADE, db_column='Workingstatus_Id')
    Product_Id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='Product_Id')
    Customer_Id = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='Customer_Id')
    CreatedDate = models.DateTimeField(default=timezone.now())
    CreatedDateOrigin = models.DateTimeField(default=timezone.now())
    Deadline = models.IntegerField()
    Donhang_Require = models.CharField(max_length=1000)
    Donhang_Price_Combo = models.BigIntegerField()
    Donhang_Price_Discount = models.BigIntegerField()
    Donhang_Price_Upsale = models.BigIntegerField()
    Donhang_Price_Payment = models.BigIntegerField()
    IsDelete = models.IntegerField(default=0)
    LastUpdate = models.DateTimeField(default=timezone.now())
    Username = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User')
    Image1 = models.CharField(max_length=1000,null=True, blank=True)
    Image2 = models.CharField(max_length=1000, null=True, blank=True)
    Image3 = models.CharField(max_length=1000, null=True, blank=True)
    Image4 = models.CharField(max_length=1000, null=True, blank=True)
    Image5 = models.CharField(max_length=1000, null=True, blank=True)
    Image6 = models.CharField(max_length=1000, null=True, blank=True)

    # PaymentStatus_Id = models.ForeignKey(Paymentstatus, on_delete=models.CASCADE, db_column='Paymentstatus_Id')

    def __str__(self):
        return self.Donhang_Name