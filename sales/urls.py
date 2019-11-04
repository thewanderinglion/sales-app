from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='sales-home'),
    path('about/', views.about, name='sales-about'),
    path('customer/', views.customer, name='sales-customer'),
    path('order/', views.order, name='sales-order'),
    path('payment/', views.payment, name='sales-payment'),
    path('customer-registration/', views.customer_registration, name='customer-registration'),
    path('order-placement/', views.order_placement, name='order-placement'),
    path('payment-accept/', views.payment_accept, name='payment-accept')
]