# Generated by Django 5.1.4 on 2025-01-01 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('systemapp', '0003_remove_cart_created_at_remove_cart_is_ordered_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='status',
            new_name='delivery_status',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='total',
            new_name='total_price',
        ),
    ]