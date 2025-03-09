from rest_framework import serializers
from .models import TrackingData

class TrackingDataSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()  # Tambahkan field status

    class Meta:
        model = TrackingData
        fields = "__all__"  # Pastikan semua field tetap ada

    def get_status(self, obj):
        return "active" if obj.speed > 0 else "offline"  # Speed > 0 = active, else offline
