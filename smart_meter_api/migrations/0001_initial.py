# Generated by Django 4.2 on 2023-04-25 17:58

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("_id", models.CharField(blank=True, max_length=64, null=True)),
                ("eui", models.CharField(blank=True, max_length=128, null=True)),
                ("time", models.DateTimeField(null=True)),
                ("rssi", models.IntegerField(null=True)),
                ("freq", models.FloatField(null=True)),
                ("chan", models.IntegerField(null=True)),
                ("snr", models.FloatField(null=True)),
                ("payload", models.CharField(blank=True, max_length=512, null=True)),
                ("size", models.IntegerField(null=True)),
                ("dat_rate", models.CharField(blank=True, max_length=20, null=True)),
                ("mod", models.CharField(blank=True, max_length=10, null=True)),
                ("createdAt", models.DateTimeField(auto_now_add=True, null=True)),
                ("updatedAt", models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
