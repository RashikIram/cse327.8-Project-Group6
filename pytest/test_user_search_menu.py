from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from Coffee_Shop_Management.models import Order, Paycheck, Menu
from Coffee_Shop_Management.views import user_search_menu
import pytest
from decimal import Decimal

@pytest.mark.django_db
def test_user_search_menu(client):
    user = User.objects.create_user(username='MMA1', password='siristhebest123')

    menu_item = Menu.objects.create(name='Test Item', price=10.0, picture='test.jpg')

    # Log in as the user and send a POST request
    client.login(username='MMA1', password='siristhebest123')
    response = client.post('/userSearchMenu', {'searched': 'Test'})

    # Checking if the response is a success
    assert response.status_code == 200

    # Checking if 'searched' is set to the expected value
    assert response.context['searched'] == 'Test'

    # Checking if the 'menuResult' contains the menu item then it will be displayed
    menu_result = response.context['menuResult']
    assert menu_item in menu_result