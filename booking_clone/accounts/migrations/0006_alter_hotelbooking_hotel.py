# Generated by Django 5.1.6 on 2025-03-09 03:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_hotelbooking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelbooking',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='accounts.hotel'),
        ),
    ]
