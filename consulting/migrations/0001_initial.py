# Generated by Django 3.2.12 on 2022-07-22 17:51

import consulting.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consultant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('cv', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultantFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=consulting.models.consultant_file_directory_path)),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='consulting.consultant')),
            ],
        ),
    ]
