# Generated by Django 5.1.4 on 2025-01-13 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='orderId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='orders.order'),
        ),
    ]