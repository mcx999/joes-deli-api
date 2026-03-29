from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({"message": "Welcome to Little Lemon API"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('LittleLemonDRF.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', root_view),  # ✅ This handles GET /
    # Add other paths as needed
]

