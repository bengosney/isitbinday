# Django
from django.db import transaction
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

# Third Party
from rest_framework import serializers

# First Party
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    url_template = serializers.CharField(max_length=512, write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "url_template")
        extra_kwargs = {
            "email": {"required": True, "allow_blank": False},
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "password": {"write_only": True},
        }

    @transaction.atomic
    def create(self, validated_data):
        url_template = validated_data.pop("url_template")
        validated_data["username"] = validated_data["email"]
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.is_active = False
        user.set_password(password)
        user.save()
        user.send_auth_email(url_template)
        # try:
        # except Exception as e:
        #     return {"error": f"{e}"}

        return user


class AcctivateSerializer(serializers.Serializer):
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    email = serializers.EmailField(read_only=True)

    def create(self, validated_data):
        try:
            uid = force_str(urlsafe_base64_decode(validated_data["uid"]))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and user.activate(validated_data["token"]):
            return user

        return {"error": "Could not activate user"}
