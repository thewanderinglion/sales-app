from django import forms
from .models import Customer, Order, Payment
from django.forms import ModelForm

# Here we are defining 3 forms: one to create a new customer, one to place a new order, and one to receive a payment
# The database relations between these 3 forms are defined at models.py

class CustomerRegistrationForm(ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'email'
        ]


class OrderPlacementForm(ModelForm):
    customer = forms.ModelChoiceField(Customer.objects)
    product = forms.CharField(max_length=225)
    product_sale_price = forms.DecimalField(label='Product Sale Price in $', max_digits=19, decimal_places=2)

    class Meta:
        model = Order
        fields = [
            'customer',
            'product',
            'product_sale_price'
        ]


class PaymentAcceptForm(ModelForm):
    order = forms.ModelChoiceField(Order.objects)
    customer = forms.ModelChoiceField(Customer.objects)
    payment_type = forms.ChoiceField(choices=[('Cash', 'Cash'), ('Card', 'Card')])
    payment_amount = forms.DecimalField(label='Payment Amount in $', max_digits=19, decimal_places=2)

    class Meta:
        model = Payment
        fields = [
            'order',
            'customer',
            'payment_type',
            'payment_amount'
        ]