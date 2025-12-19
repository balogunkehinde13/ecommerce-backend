from django.urls import path
from .views import (
    UserRegistrationView,
    UserProfileView,
    UserListView
)

urlpatterns = [
    # POST → Register new user
    path('register/', UserRegistrationView.as_view(), name='user-register'),

    # GET / PUT → View or update logged-in user's profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    # GET → List all users (authentication required)
    path('users/', UserListView.as_view(), name='user-list'),
]
