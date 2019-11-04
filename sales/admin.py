from django.contrib import admin
from .models import Customer, Order, Payment


class CustomerAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'amount_owed']
    readonly_fields = ['amount_owed']


admin.site.register(Customer, CustomerAdmin)


class OrderAdmin(admin.ModelAdmin):
    fields = ['customer', 'product', 'product_sale_price', 'date_bought', 'amount_owed', 'payments_total']
    readonly_fields = ['date_bought', 'amount_owed', 'payments_total']


admin.site.register(Order, OrderAdmin)


class PaymentAdmin(admin.ModelAdmin):
    fields = ['order', 'customer', 'payment_type', 'payment_amount', 'date_paid']
    readonly_fields = ['date_paid']


admin.site.register(Payment, PaymentAdmin)
