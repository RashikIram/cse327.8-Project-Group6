from django.contrib import admin
from django.db import models
from .models import Menu, Order, Paycheck

# Register your models here.




admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(Paycheck)

