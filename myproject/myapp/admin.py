from django.contrib import admin
from .models import *

# Register your models here.




admin.site.register(user)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(wishlistItem)
admin.site.register(CheckoutDetails)
admin.site.register(contacts)
admin.site.register(Order)
admin.site.register(Subscribes)