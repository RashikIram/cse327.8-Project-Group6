from django.contrib import admin
from django.db import models
from .models import Menu
# Register your models here.
class MenuAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'item_name',
                    'price', 'item_picture')


admin.site.register(Menu, MenuAdmin)

