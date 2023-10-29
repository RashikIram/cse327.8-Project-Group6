from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from django.test import RequestFactory
from Coffee_Shop_Management.models import Order, Paycheck, Menu
from Coffee_Shop_Management.views import add_to_cart
import pytest
from decimal import Decimal

@pytest.mark.django_db
def test_add_to_cart():
    # At first creating a user
    user = User.objects.create_user(username='testuser', password='testpassword')

    # Creating a menu item
    menu_item = Menu.objects.create(name='Test Item', price=10.0, picture='test.jpg')

    # Creating a mock request using RequestFactory
    factory = RequestFactory()
    request = factory.get('/')
    request.user = user  # Set the user attribute on the request

    # Calling the add_to_cart view with the mock request
    response = add_to_cart(request, item_id=menu_item.id)

    # Checking if the item was added to the cart then cart will be shown
    order = Order.objects.filter(items=menu_item, customer=user).first()
    assert order is not None
    assert order.quantity == 1