# Generated by Django 5.1.6 on 2025-02-20 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_hoteluser_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelvendor',
            name='business_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotelvendor',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
