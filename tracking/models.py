from django.db import models
from .utils import send_over_speeding_alert, send_telegram_alert

class TrackingData(models.Model):
    device_id = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    over_speeding = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.speed > 100:
            self.over_speeding = True
            send_over_speeding_alert(self.device_id, self.speed, self.timestamp)  # Kirim notifikasi 🚨
            send_telegram_alert(self.device_id, self.speed, self.timestamp)  # Kirim Telegram 🚀

        super().save(*args, **kwargs)
