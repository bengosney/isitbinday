# Third Party
from rest_framework import serializers

# Locals
from .models import AuthDetails, HomeGroup, User


class HomeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeGroup
        fields = ["name"]


class AuthDetailsSerializer(serializers.ModelSerializer):
    homeGroups = HomeGroupSerializer(many=True)

    class Meta:
        model = AuthDetails
        fields = ["homeGroups"]


class UserSerializer(serializers.ModelSerializer):
    authdetails = AuthDetailsSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "authdetails",
        ]
