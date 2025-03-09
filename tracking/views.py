from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

from .models import TrackingData
from .serializers import TrackingDataSerializer
from .utils import update_ship_location, get_ship_location


# Custom Pagination (10 data per halaman)
class TrackingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class TrackingDataViewSet(viewsets.ModelViewSet):
    queryset = TrackingData.objects.all().order_by('-timestamp')
    serializer_class = TrackingDataSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp']
    pagination_class = TrackingPagination  # Tambahkan pagination

    # Filter berdasarkan device_id + Pagination
    @action(detail=False, methods=['get'])
    def by_device(self, request):
        device_id = request.query_params.get('device_id')
        limit = request.query_params.get('limit', 10)  # Ambil 'limit' dari URL, default = 10

        if not device_id:
            return Response({"error": "device_id parameter is required"}, status=400)

        queryset = TrackingData.objects.filter(device_id=device_id).order_by('-timestamp')[:int(limit)]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# ✅ Simpan lokasi kapal ke Redis
@method_decorator(csrf_exempt, name='dispatch')
class UpdateLocationView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            ship_id = data.get("ship_id")
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if not ship_id or latitude is None or longitude is None:
                return JsonResponse({"error": "Missing parameters"}, status=400)

            update_ship_location(ship_id, latitude, longitude)
            return JsonResponse({"message": "Location updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# ✅ Ambil lokasi kapal dari Redis
@method_decorator(csrf_exempt, name='dispatch')
class GetLocationView(View):
    def get(self, request, ship_id, *args, **kwargs):
        location = get_ship_location(ship_id)
        if location:
            return JsonResponse({"ship_id": ship_id, "location": location})
        return JsonResponse({"error": "Ship not found"}, status=404)
