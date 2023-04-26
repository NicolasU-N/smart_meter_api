from django.db import models


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    _id = models.CharField(max_length=64, blank=True, null=True)
    eui = models.CharField(max_length=128, blank=True, null=True)
    time = models.DateTimeField(null=True)
    rssi = models.IntegerField(null=True)
    freq = models.FloatField(null=True)
    chan = models.IntegerField(null=True)
    snr = models.FloatField(null=True)
    payload = models.CharField(max_length=512, blank=True, null=True)
    size = models.IntegerField(null=True)
    dat_rate = models.CharField(max_length=20, blank=True, null=True)
    mod = models.CharField(max_length=10, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.EUI} at {self.time}"
        # return self

    def save(self, *args, **kwargs):
        # Implement any custom save logic here
        super().save(*args, **kwargs)
