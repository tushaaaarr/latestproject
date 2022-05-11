# Generated by Django 3.1.7 on 2021-11-03 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0029_placedorders_inbox_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='placedorders',
            old_name='status',
            new_name='deliver_status',
        ),
        migrations.AddField(
            model_name='placedorders',
            name='on_way_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='placedorders',
            name='order_picked_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='placedorders',
            name='reached_location_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='placedorders',
            name='store_status',
            field=models.BooleanField(default=False),
        ),
    ]
