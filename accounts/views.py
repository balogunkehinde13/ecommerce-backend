from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    Handles new user registration.
    No authentication required.

    Validates password strength, ensures passwords match,
    and returns newly created user information.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()  # create_user() already hashes passwords

        return Response({
            "message": "User registered successfully.",
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)



class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Allows authenticated users to view or update
    their own profile information.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # User can ONLY access their own profile
        return self.request.user



class UserListView(generics.ListAPIView):
    """
    Admin-only endpoint to view all registered users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Optionally restrict to admin
