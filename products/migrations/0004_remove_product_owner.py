# Generated by Django 4.0.4 on 2022-06-01 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_farm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='owner',
        ),
    ]
