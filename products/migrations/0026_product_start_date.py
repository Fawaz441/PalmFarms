# Generated by Django 3.2.12 on 2022-07-29 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20220728_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]