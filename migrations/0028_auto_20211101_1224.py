# Generated by Django 3.1.7 on 2021-11-01 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0027_auto_20211030_2027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='placedorders',
            old_name='state',
            new_name='city',
        ),
    ]
