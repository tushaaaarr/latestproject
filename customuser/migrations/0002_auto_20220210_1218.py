# Generated by Django 3.1.7 on 2022-02-10 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cities',
            name='state',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='deliverypartner',
            name='username',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='getdeliveries',
            name='customername',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='getdeliveries',
            name='deliverusername',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='getdeliveries',
            name='storeuser',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='image',
            name='store_user',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='image',
            name='user',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='notification',
            name='reciver',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='notification',
            name='sender',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='orders',
            name='c_username',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='orders',
            name='d_username',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='orders',
            name='s_username',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='email',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='username',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='placedorders',
            name='customername',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='placedorders',
            name='username',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='reciver',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='sender',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='profile',
            name='otp',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='savedaddress',
            name='username',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='shop',
            name='store_user',
            field=models.CharField(max_length=40),
        ),
    ]
