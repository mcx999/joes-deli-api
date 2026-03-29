from djoser.serializers import TokenCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers


class CustomTokenCreateSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("✅ CustomTokenCreateSerializer is active")  # Debug print
        data = super().validate(attrs)
        refresh = RefreshToken.for_user(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data









