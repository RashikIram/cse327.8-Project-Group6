from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):
    """
    This model is representing the menu items.

    :param name: The name of the menu item.
    :type name: str, max length 255.

    :param price: The price of the menu item.
    :type price: Decimal with max digits 10 and 2 decimal places.

    :param picture: An image representing the menu item.
    :type picture: ImageField.

    :meta: Class for specifying database table name.

    :classmethod get_items_by_id: Get menu items by their IDs.
    :classmethod get_all_products: Get all menu items.
    """
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    picture = models.ImageField(upload_to='menu_pictures/')

    class Meta:
        db_table = 'menu'

    @staticmethod
    def get_items_by_id(item_id):
        return Menu.objects.filter(id__in=item_id)

    @staticmethod
    def get_all_products():
        return Menu.objects.all()

class Order(models.Model):
    """
    This model is representing customer orders.

    :param items: The menu item in the order.
    :type items: ForeignKey to Menu.

    :param customer: The user who placed the order.
    :type customer: ForeignKey to User.

    :param quantity: The quantity of the menu item in the order.
    :type quantity: int, default 1.

    :param price: The total price of the order.
    :type price: Decimal with max digits 10 and 2 decimal places.

    :param address: The delivery address for the order.
    :type address: str, max length 50, default blank.

    :param phone: The contact phone number for the order.
    :type phone: str, max length 50, default blank.
    """
    items = models.ForeignKey(Menu, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)

class Paycheck(models.Model):
    """
    This model is representing staff paychecks.

    :param staff: The staff member for whom the paycheck is issued.
    :type staff: ForeignKey to User.

    :param total_cost: The total earnings for the staff.
    :type total_cost: Decimal with max digits 10 and 2 decimal places, default 0.00, nullable.
    """
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)