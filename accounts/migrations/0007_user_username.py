# Generated by Django 3.2.12 on 2022-07-22 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20220722_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
