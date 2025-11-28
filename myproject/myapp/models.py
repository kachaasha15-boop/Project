from django.db import models
from datetime import datetime

# Create your models here.

class user(models.Model):
    name= models.CharField(max_length=50)
    email= models.EmailField(max_length=50)
    password= models.CharField(max_length=50)
    phone_number=models.IntegerField(blank=True,null=True)
    image=models.ImageField(upload_to='image', blank=True,null=True)
    otp=models.IntegerField(blank=True,null=True)


class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.ImageField(upload_to="image")


class CartItem(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.IntegerField(blank=True,null=True)
    is_active = models.BooleanField(default=True) 

class wishlistItem(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class CheckoutDetails(models.Model):
    country = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)  
    address = models.CharField(max_length=50)
    state_country = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=50)
    phone = models.IntegerField(blank=True, null=True)

class contacts(models.Model):
    f_name=models.CharField(max_length=50)
    l_name=models.CharField(max_length=50)
    e_address=models.EmailField(max_length=50)
    message=models.CharField(max_length=50)

class Order(models.Model):  
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    address = models.ForeignKey(CheckoutDetails, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)  
    subtotal = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(default=datetime.now)

class Subscribes(models.Model):
    name= models.CharField(max_length=50)
    email= models.EmailField(max_length=60)
