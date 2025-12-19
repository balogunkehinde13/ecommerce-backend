from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')

urlpatterns = [
       # 👇 CUSTOM ROUTES MUST COME FIRST
    path('wishlist/', include('products.wishlist_urls')),

    # 👇 Router goes LAST
    path('', include(router.urls)),
]
