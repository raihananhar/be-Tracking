from celery import shared_task
import random
from .models import TrackingData

@shared_task
def update_location():
    # Ambil semua tracking data
    tracking_items = TrackingData.objects.all()

    # Update lokasi barang random (contoh aja)
    for item in tracking_items:
        item.latitude += random.uniform(-0.01, 0.01)  # Geser dikit lat
        item.longitude += random.uniform(-0.01, 0.01)  # Geser dikit lon
        item.save()
    
    return "Tracking data updated!"
