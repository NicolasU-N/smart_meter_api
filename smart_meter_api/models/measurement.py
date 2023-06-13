import json
from django.db import models
from .device import Device


class Measurement(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    rssi = models.IntegerField(null=True)
    snr = models.FloatField(null=True)
    modinfo = models.CharField(max_length=64, blank=True, null=True)
    codrate = models.CharField(max_length=32, blank=True, null=True)
    freq = models.FloatField(null=True)
    size = models.IntegerField(null=True)
    volume = models.FloatField(null=True)
    battery_level = models.FloatField(null=True)
    payload = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Measurement for {self.device} at {self.timestamp}"

    def save(self, *args, **kwargs):
        if self.payload:
            try:
                payload_json = json.loads(self.payload)
                # print("in models: ", payload_json)
                self.volume = payload_json["vol"]
                self.battery_level = payload_json["batt_lvl"]
            except json.JSONDecodeError:
                print("ERROR JSON LOAD IN MODELS")
                pass
        super().save(*args, **kwargs)
