from django.db import models

# Create your models here.


class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)



class Menu(models.Model):
    item_id = models.IntegerField(primary_key=True)
    item_name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    item_picture = models.ImageField(upload_to='menu_pictures/')  # Use ImageField

    class Meta:
        db_table = 'menu'

    @staticmethod
    def get_items_by_id(item_id):
        return Menu.objects.filter(id__in =item_id)

    @staticmethod
    def get_all_products():
        return Menu.objects.all()