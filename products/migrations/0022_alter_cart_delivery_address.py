# Generated by Django 3.2.12 on 2022-07-25 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dispatching', '0002_auto_20220725_1940'),
        ('products', '0021_remove_coupon_single_use'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='delivery_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dispatching.dispatchaddress'),
        ),
    ]
