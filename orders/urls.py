from django.urls import path
from .views import CreateOrderView, OrderListView

urlpatterns = [
    # POST → Create a new order from user's cart
    path('create/', CreateOrderView.as_view(), name='order-create'),

    # GET → Order history for logged-in user
    path('', OrderListView.as_view(), name='order-list'),
]
