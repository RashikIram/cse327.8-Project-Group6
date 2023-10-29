from django.db import models
from django.contrib.auth.models import User  






class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    picture = models.ImageField(upload_to='menu_pictures/')  # Use ImageField

    class Meta:
        db_table = 'menu'

    @staticmethod
    def get_items_by_id(item_id):
        return Menu.objects.filter(id__in =item_id)

    @staticmethod
    def get_all_products():
        return Menu.objects.all()

class Order(models.Model):
    items = models.ForeignKey(Menu, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)

class Paycheck(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)  
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)