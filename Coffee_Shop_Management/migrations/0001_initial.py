# Generated by Django 4.2.6 on 2023-10-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('item_id', models.IntegerField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=255, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item_picture', models.ImageField(upload_to='menu_pictures/')),
            ],
            options={
                'db_table': 'menu',
            },
        ),
    ]
