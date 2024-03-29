# Generated by Django 4.0.4 on 2022-05-31 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_farm'),
        ('products', '0002_alter_producttype_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='farm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='farm_products', to='accounts.farm'),
        ),
    ]
