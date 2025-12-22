from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

# JWT Authentication views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

@api_view(['GET'])
def api_root(request):
    """API root endpoint with available routes"""
    return Response({
        'message': 'Welcome to E-commerce API',
        'endpoints': {
            'admin': '/admin/',
            'token_obtain': '/api/token/',
            'token_refresh': '/api/token/refresh/',
            'accounts': '/api/accounts/',
            'products': '/api/products/',
            'categories': '/api/categories/',
            'cart': '/api/cart/',
            'orders': '/api/orders/',
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),  # ADD THIS LINE
    path('admin/', admin.site.urls),

    # -------------------------------
    # AUTHENTICATION (JWT)
    # -------------------------------
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # -------------------------------
    # APP ROUTES
    # -------------------------------
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)