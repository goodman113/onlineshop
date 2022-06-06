from distutils.command.upload import upload
import email
from email.mime import image
from itertools import product
from pyexpat import model
from statistics import quantiles
from tokenize import blank_re
from traceback import print_exc
from unicodedata import category
from venv import create
from xml.dom.pulldom import default_bufsize
from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    image= models.ImageField(upload_to='category',null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self) -> str:
        return self.name

class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=199, null=True,  blank=True)
    price = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    stock = models.IntegerField(default=0, null=True, blank=True)
    status = models.BooleanField(default=True)

    def real_price(self):
        return self.price-(self.stock*self.price)/100

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.product.name

class Orders(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    done_status = models.BooleanField(default=False)
    first_name = models.CharField(max_length=125, null=True, blank=True)
    last_name = models.CharField(max_length=125, null=True, blank=True)
    email = models.CharField(max_length=125, null=True, blank=True)
    number = models.CharField(max_length=125, null=True, blank=True)
    viloyat = models.CharField(max_length=125, null=True, blank=True)
    address1 = models.CharField(max_length=225, null=True, blank=True)
    address2 = models.CharField(max_length=225, null=True, blank=True)
    postal_code = models.CharField(max_length=125, null=True, blank=True)


    def __str__(self):
        return f"{self.customer.first_name}  {self.done_status}"

class Order_details(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(null=True, blank=True, default=0)
    quantity = models.IntegerField(blank=True, null=True, default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def sold_price(self):
        return self.price*self.quantity

    @property
    def real_price(self):
        return self.product.price * self.quantity

    def __str__(self) :
        return f"{self.order.customer.first_name} {self.product.name}"

class States(models.Model):
    name = models.CharField(max_length=199, blank=True, null=True)

    def __str__(self) :
        return f"{self.name}"
        
class Country(models.Model):
    name = models.CharField(max_length=199, blank=True, null=True)

    def __str__(self) :
        return f"{self.name}"