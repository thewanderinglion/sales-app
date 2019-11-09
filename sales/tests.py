from django.test import TestCase
from django.urls import reverse
'''
These tests test whether the URLs return HTTPResponse of 200 (meaning the request has succeeded)
'''
class ViewsResponsivenessTest(TestCase):
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