from accounts.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework import serializers

# User Serializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("id","username", "email", "password", "password2", "bio", "profile_image")

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match")
        if CustomUser.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email is already in use.")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        return CustomUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get("username"), password=data.get("password")
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "user_type", "bio", "profile_image")
        read_only_fields = ("id", "username", "email", "user_type")
