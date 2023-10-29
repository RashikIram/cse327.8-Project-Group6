from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from Coffee_Shop_Management.models import Paycheck
from Coffee_Shop_Management.views import view_earnings
import pytest
from decimal import Decimal

@pytest.mark.django_db
def test_view_earnings():
    client = Client()
    user = User.objects.create_user(username='MMA1', password='sir1234')
    paycheck = Paycheck.objects.create(staff=user, total_cost=0.0)
    #Logging in as a staff 
    client.login(username='MMA1', password='sir1234')
    response = client.get('/view_earnings/')  
    #Response to be shown if earnings can be viewed
    assert response.status_code == 200