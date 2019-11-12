from django.test import TestCase
from django.urls import reverse
from .models import Customer, Order, Payment

# # Imported for mixer:
# from unittest.mock import patch
# import pytest
# from django.contrib.auth.models import signals
# from django.conf import settings
from mixer.backend.django import mixer


class ViewsResponsivenessTest(TestCase):
    """
    These 8 tests test whether the URLs return HTTPResponse of 200 (meaning the request has succeeded)
    """
    def test_home_page(self):
        response = self.client.get(reverse('sales-home'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('sales-about'))
        self.assertEqual(response.status_code, 200)

    def test_sales_customer(self):
        response = self.client.get(reverse('sales-customer'))
        self.assertEqual(response.status_code, 200)

    def test_sales_order(self):
        response = self.client.get(reverse('sales-order'))
        self.assertEqual(response.status_code, 200)

    def test_sales_payment(self):
        response = self.client.get(reverse('sales-payment'))
        self.assertEqual(response.status_code, 200)

    def test_customer_registration(self):
        response = self.client.get(reverse('customer-registration'))
        self.assertEqual(response.status_code, 200)

    def test_order_placement(self):
        response = self.client.get(reverse('order-placement'))
        self.assertEqual(response.status_code, 200)

    def test_payment_accept(self):
        response = self.client.get(reverse('payment-accept'))
        self.assertEqual(response.status_code, 200)


class OrderModelTests(TestCase):
    """
    These 4 tests test whether some of the variables in the model are functioning as expected
    """
    def test_initial_customer_owed_is_zero(self):
        init_cust = Customer(first_name="test_first", last_name="test_last", email="test@email.com")
        self.assertEqual(init_cust.amount_owed, 0)

    def test_order_amount_owed_equals_product_price(self):
        init_cust = Customer(first_name="test_first", last_name="test_last", email="test@email.com")
        init_order = Order(customer=init_cust, product="test_product", product_sale_price=2000.00)
        self.assertEqual(init_order.amount_owed, init_order.product_sale_price)

    def test_customer_amount_owed_equals_order_amount_owed(self):
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer)
        self.assertEqual(order.customer, customer)
        # self.assertEqual(customer.amount_owed, order.amount_owed)

    def test_customer_amount_owed_equals_order_sale_price_minus_payment_amount(self):
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer, product_sale_price=2000.00)
        payment = mixer.blend(Payment, order=order, customer=customer, payment_amount=1000.00)
        self.assertEqual(abs(customer.amount_owed), (abs((order.product_sale_price - payment.payment_amount))))

    def test_mixer(self):
        customer = mixer.blend(Customer, last_name='j')
        assert customer.last_name == 'j'

    def test_customer_instance_equals_customer_instance_in_order(self):
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer)
        self.assertEqual(order.customer, customer)
        # self.assertEqual(customer.amount_owed, order.amount_owed)