from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes basic user information.
    Used for:
    - Returning the logged-in user's profile
    - Displaying user info in orders
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']



class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles user signup.
    Includes:
    - Password validation
    - Password confirmation field
    - Automatic user creation
    """

    # write_only → do not return passwords in responses
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]  # Built-in Django validators
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email',
            'password', 'password2',
            'first_name', 'last_name'
        ]

    def validate(self, attrs):
        """
        Ensure both passwords match before saving.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })
        return attrs

    def create(self, validated_data):
        """
        Removes password2 and uses create_user()
        so password is hashed correctly.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
