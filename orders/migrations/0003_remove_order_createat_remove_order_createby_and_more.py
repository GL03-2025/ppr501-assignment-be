# Generated by Django 5.1.4 on 2025-01-12 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='createAt',
        ),
        migrations.RemoveField(
            model_name='order',
            name='createBy',
        ),
        migrations.RemoveField(
            model_name='order',
            name='deleteAt',
        ),
        migrations.RemoveField(
            model_name='order',
            name='deleteBy',
        ),
        migrations.RemoveField(
            model_name='order',
            name='updateAt',
        ),
        migrations.RemoveField(
            model_name='order',
            name='updateBy',
        ),
    ]
