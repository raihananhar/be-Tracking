from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackingDataViewSet, UpdateLocationView, GetLocationView

router = DefaultRouter()
router.register(r'tracking', TrackingDataViewSet, basename='tracking')

urlpatterns = [
    path('update-location/', UpdateLocationView.as_view(), name='update_location'),
    path('get-location/<str:ship_id>/', GetLocationView.as_view(), name='get_location'),
] + router.urls
