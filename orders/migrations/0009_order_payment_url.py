# Generated by Django 5.1.4 on 2025-01-13 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0008_order_method_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
