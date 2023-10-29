from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from Coffee_Shop_Management.models import Order, Paycheck, Menu
import pytest
from decimal import Decimal

@pytest.mark.django_db
def test_menu():
    # Creating a user and a menu item
    user = User.objects.create_user(username='MMA1', password='siristhebest123')
    menu_item = Menu.objects.create(name='Test Item', price=10.0, picture='test.jpg')

    # Creating a client and log in
    client = Client()
    client.login(username='MMA1', password='siristhebest123')

    # Making a GET request to the menu view then the menu item will be shown in menu
    response = client.get('/menu')