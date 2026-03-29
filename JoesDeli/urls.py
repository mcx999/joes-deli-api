from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from JoesDeliDRF.views import GroupManagementViewSet

# Group management viewset mapping
group_management = GroupManagementViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})

# Root welcome view
def root_view(request):
    return JsonResponse({"message": "Welcome to Joe's Deli API"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('JoesDeliDRF.urls')),
    # Comment out or remove these to avoid conflicts with your custom token view
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),
    # Comment out or remove this line to avoid conflict with your custom token create view
    path('auth/', include('djoser.urls.jwt')),
    path('', root_view),
    path('api/groups/<str:group_name>/users/', group_management),
    path('api/groups/<str:group_name>/users/<int:user_id>/', group_management),
]