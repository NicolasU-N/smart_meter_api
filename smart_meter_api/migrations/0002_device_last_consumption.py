# Generated by Django 4.2 on 2023-06-01 22:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("smart_meter_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="device",
            name="last_consumption",
            field=models.FloatField(null=True),
        ),
    ]