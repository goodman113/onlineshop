# Generated by Django 4.0.4 on 2022-05-22 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_products_quantity_products_status_orders_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_details',
            name='price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
