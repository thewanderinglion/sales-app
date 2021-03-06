from mixer.backend.django import mixer
from django.db.models import DateTimeField
from django.test import TestCase
from django.urls import reverse
from .models import Customer, Order, Payment
import datetime


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
    These 14 tests test whether some of the variables in the model are functioning as expected
    """
    def test_initial_customer_owed_is_zero(self):
        init_cust = Customer(first_name="test_first", last_name="test_last", email="test@email.com")
        self.assertEqual(init_cust.amount_owed, 0)

    def test_order_amount_owed_equals_product_price(self):
        init_cust = Customer(first_name="test_first", last_name="test_last", email="test@email.com")
        init_order = Order(customer=init_cust, product="test_product", product_sale_price=2000.00)
        self.assertEqual(init_order.amount_owed, init_order.product_sale_price)

    def test_customer_ammount_owed_equals_order_sales_price_from_multiple_orders(self):
        customer = mixer.blend(Customer)
        order_1 = mixer.blend(Order, customer=customer, product_sale_price=2000.00)
        order_2 = mixer.blend(Order, customer=customer, product_sale_price=2000.00)
        print(customer.amount_owed, 4000)
        self.assertEqual(customer.amount_owed, 4000.00)

    def test_customer_amount_owed_equals_order_sale_price_minus_payment_amount(self):
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer, product_sale_price=2000.00)
        payment = mixer.blend(Payment, order=order, customer=customer, payment_amount=1000.00)
        self.assertEqual((customer.amount_owed), (order.product_sale_price - payment.payment_amount))

    def test_customer_amount_owed_equals_zero_after_full_payment(self):
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer, product_sale_price=2000.00)
        payment = mixer.blend(Payment, order=order, customer=customer, payment_amount=2000.00)
        self.assertEqual(customer.amount_owed, 0)

    def test_customer_amount_owed_can_be_negative(self):
        """
        checking if the customer amount owed becomes negative to ensure that the calculations are working
        """
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer, product_sale_price=1000.00)
        payment = mixer.blend(Payment, order=order, customer=customer, payment_amount=2000.00)
        self.assertLess(customer.amount_owed, 0)

    def test_mixer(self):
        customer = mixer.blend(Customer, last_name='j')
        assert customer.last_name == 'j'

    def test_customer_instance_equals_customer_instance_in_order(self):
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer)
        self.assertEqual(order.customer, customer)

    def test_order_date_field_is_being_automatically_populated(self):
        """
        testing to check if the date field is being populated
        """
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer, product_sale_price=3000.00)
        self.assertIsInstance(order.date_bought, datetime.datetime)

    def test_payment_date_field_is_being_automatically_populated(self):
        """
        testing to check if the date field is being populated
        """
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer, product_sale_price=3000.00)
        payment = mixer.blend(Payment, order=order, customer=customer, payment_amount=3000.00)
        self.assertIsInstance(order.date_bought, datetime.datetime)

    def test_order_date_field_is_current_date(self):
        """
        Testing to check if the generated date field in orders is today's date
        """
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer, product_sale_price=3000.00)
        self.assertEqual(order.date_bought.date(), datetime.datetime.now().date())

    def test_payment_date_field_is_current_date(self):
        """
        Testing to check if the generated date field in payments is today's date
        """
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer, product_sale_price=3000.00)
        payment = mixer.blend(Payment, order=order, customer=customer, payment_amount=3000.00)
        self.assertEqual(payment.date_paid.date(), datetime.datetime.now().date())

    def test_order_date_field_is_equal_to_payment_date_if_order_is_paid_immediately(self):
        """
        Testing to check if the date field in Orders equals date field in Payments if customer pays on the spot
        The test is passing now, alhamdulillah! Added .date() to compare
        """
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer, product_sale_price=3000.00)
        payment = mixer.blend(Payment, order=order, customer=customer, payment_amount=3000.00)
        self.assertEqual(order.date_bought.date(), payment.date_paid.date())

    def test_payment_date_is_later_than_order_date(self):
        """
        how do I create a payment with date_paid in Mixer 7 days in the future?
        this test will work very well with live data. if the test fails, then that means users are creating payments
        without associated orders
        """
        customer = mixer.blend(Customer)
        order = mixer.blend(Order, customer=customer, product_sale_price=3000.00)
        now = datetime.datetime.now()
        future = now + datetime.timedelta(days=7)
        payment = mixer.blend(Payment, order=order, customer=customer, payment_amount=3000.00, date_paid=future)
        self.assertLess(order.date_bought, payment.date_paid)

    def test_whether_app_can_process_large_number_of_orders(self):
        """
        generating 1000 orders then verifying if all of them correctly generated
        ***excellent code to review many Python techniques
        """
        order_list = []
        def count_order():
            for i in range(1000):
                customer = mixer.blend(Customer)
                order = mixer.blend(Order, customer=customer, product_sale_price=1.00)
                order_list.append(order)
            return len(order_list)
        # print("checking count", count_order())
        self.assertEqual(count_order(), 1000)

    def test_whether_app_can_process_large_number_of_payments(self):
        payment_list = []
        def count_payments():
            for i in range(1000):
                customer = mixer.blend(Customer)
                order = mixer.blend(Order, customer=customer, product_sale_price=1.00)
                payment = mixer.blend(Payment, order=order, customer=customer, payment_amount=1.00)
                payment_list.append(payment)
            return len(payment_list)
        self.assertEqual(count_payments(), 1000)

