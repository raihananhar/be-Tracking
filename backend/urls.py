from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Backend is running!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tracking.urls')),
    path('', home),  # Tambahin ini buat handle root URL `/`
]