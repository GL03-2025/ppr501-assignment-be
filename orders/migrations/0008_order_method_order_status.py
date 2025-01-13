# Generated by Django 5.1.4 on 2025-01-13 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0007_remove_order_method_remove_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="method",
            field=models.CharField(
                choices=[("vnpay", "Vnpay"), ("cash", "Cash"), ("nopay", "Nopay")],
                default="nopay",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[("unpaid", "Unpaid"), ("failed", "Failed"), ("paid", "Paid")],
                default="unpaid",
                max_length=100,
            ),
        ),
    ]