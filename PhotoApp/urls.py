from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhotoViewSet

router = DefaultRouter()
router.register(r'photos', PhotoViewSet, basename='photo')  # Use singular 'photo'

urlpatterns = [
    path('api/', include(router.urls)),
]