from django.contrib import admin
from .models import Customer, Order, Payment

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Payment)
