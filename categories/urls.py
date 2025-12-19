from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

# Router automatically creates CRUD routes for the viewset
router = DefaultRouter()
router.register(r'', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
