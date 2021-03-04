# Django
from django.contrib.auth.models import User

# Third Party
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")
        extra_kwargs = {
            "email": {"required": True, "allow_blank": False},
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        validated_data["username"] = validated_data["email"]
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
