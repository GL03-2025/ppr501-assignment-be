# Generated by Django 5.1.4 on 2025-01-13 13:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0014_remove_order_order_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_uuid",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
