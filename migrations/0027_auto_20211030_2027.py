# Generated by Django 3.1.7 on 2021-10-30 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0026_auto_20211030_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='getdeliveries',
            name='is_reached_store',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='getdeliveries',
            name='is_reached_user',
            field=models.BooleanField(default=False),
        ),
    ]