# Generated by Django 4.0.4 on 2022-05-31 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttype',
            name='name',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
