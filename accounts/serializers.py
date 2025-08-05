from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'email', 'contact_number',
            'profile_picture', 'is_active', 'is_staff',
            'otp', 'otp_expired'
        ]
        read_only_fields = ['id', 'is_active', 'is_staff', 'otp', 'otp_expired']
