from django.shortcuts import render, redirect
from .models import Customer, Order, Payment
from django.contrib import messages
from .forms import CustomerRegistrationForm, OrderPlacementForm, PaymentAcceptForm


def home(request):
    return render(request, 'sales/home.html')


def about(request):
    return render(request, 'sales/about.html', {'title': 'About Our Sales'})


def customer(request):
    context = {
        'customers': Customer.objects.all(),
        'title': 'Customers'
    }
    return render(request, 'sales/customer.html', context)


def order(request):
    context = {
        'orders': Order.objects.all(),
        'title': 'Orders'
    }
    return render(request, 'sales/order.html', context)


def payment(request):
    context = {
        'payments': Payment.objects.all(),
        'title': 'Payments'
    }
    return render(request, 'sales/payment.html', context)


def customer_registration(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully created new customer!')
            return redirect('sales-customer')
    else:
        form = CustomerRegistrationForm()
    context = {'form': form, 'title': 'New Customer Registration'}
    return render(request, 'sales/customer_registration.html', context)


def order_placement(request):
    if request.method == 'POST':
        form = OrderPlacementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully placed new order!')
            return redirect('sales-order')
    else:
        form = OrderPlacementForm()
    return render(request, 'sales/order_placement.html', {'form': form, 'title': 'New Order Placement'})


def payment_accept(request):
    if request.method == 'POST':
        form = PaymentAcceptForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully accepted payment!')
            return redirect('sales-payment')
    else:
        form = PaymentAcceptForm()
    return render(request, 'sales/payment_accept.html', {'form': form, 'title': 'New Payment'})
