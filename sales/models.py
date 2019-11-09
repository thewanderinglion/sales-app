import decimal

from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    def amount_owed(self):
        """"
        This function fetches the total value of all the orders (from the Orders table) then subtracts the total value
        of all the payments (from the Payments table) to calculate the total amount a customer owes
        """
        total_cust_orders = Order.objects.filter(customer=self).aggregate(
            order_total=Coalesce(Sum('product_sale_price', output_field=models.DecimalField()), 0)
        ).get('order_total')
        total_cust_payments = Payment.objects.filter(customer=self).aggregate(
            payments_total=Coalesce(Sum('payment_amount', output_field=models.DecimalField()), 0)
        ).get('payments_total')
        return total_cust_orders - total_cust_payments

    amount_owed = property(amount_owed)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    full_name = property(full_name)

    def __str__(self):
        return f"Customer ID {self.pk}, {self.full_name}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    product = models.CharField(max_length=225)
    product_sale_price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    date_bought = models.DateTimeField(auto_now_add=True, blank=True)

    def amount_owed(self):
        """
        This function looks at the sale price of an item in the order then subtracts the amount paid for that order
        (derived from the Payment table) to calculate the amount the customer owes for this order
        """
        return decimal.Decimal(self.product_sale_price) - decimal.Decimal(self.payments_total)

    amount_owed = property(amount_owed)

    def payments_total(self):
        return Payment.objects.filter(order=self).aggregate(
            payments_total=Coalesce(Sum('payment_amount', output_field=models.DecimalField()), 0)
        ).get('payments_total')

    payments_total = property(payments_total)

    def __str__(self):
        return f"Order ID {self.pk}, {self.customer.full_name}"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    payment_type = models.CharField(max_length=25, choices=[('Cash', 'Cash'), ('Card', 'Card')], default='')
    payment_amount = models.DecimalField(max_digits=19, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"Payment ID {self.pk} for Order ID {self.order.pk}, {self.customer.full_name}"
