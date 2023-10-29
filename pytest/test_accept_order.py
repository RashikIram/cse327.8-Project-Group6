from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from Coffee_Shop_Management.models import Order,Paycheck, Menu
from Coffee_Shop_Management.views import accept_order
import pytest
from decimal import Decimal

@pytest.mark.django_db
def test_accept_order():
    client = Client()
    user = User.objects.create_user(username='Zareen', password='super123')
    menu_item = Menu.objects.create(name='Test Item', price=10.0, picture='test.jpg')
    order = Order.objects.create(items=menu_item, customer=user, quantity=1, price=10.0)
    paycheck = Paycheck.objects.create(staff=user, total_cost=0.0)
    #Logging in as staff
    client.login(username='Zareen', password='super123')
    response = client.get(f'/accept_order/{order.id}/')  
    assert response.status_code == 302  # Checking if the response is a redirect then it will be updated in paycheck