from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Order_details)
admin.site.register(States)
admin.site.register(Country)
admin.site.register(Wishlist)