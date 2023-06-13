from django.db import models


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    # _id = models.CharField(max_length=64, blank=True, null=True)
    eui = models.CharField(max_length=128, blank=True, null=True)
    last_consumption = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.eui} at {self.created_at}"

    def save(self, *args, **kwargs):
        # Implement any custom save logic here
        super().save(*args, **kwargs)

    def last_measurement(self):
        return self.measurement_set.order_by("-created_at").first()
