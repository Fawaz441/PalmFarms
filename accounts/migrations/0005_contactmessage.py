# Generated by Django 3.2.12 on 2022-06-14 01:28

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('message', models.TextField()),
            ],
        ),
    ]
