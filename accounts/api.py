# Django
from django.contrib.auth.models import User

# Third Party
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.schemas.openapi import AutoSchema

# Locals
from .serializers import ActivateSerializer, UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserActivateSchema(AutoSchema):
    def get_operation_id(self, path, method):
        return "ActivateUser"


class UserActivate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ActivateSerializer
    permission_classes = (AllowAny,)
    schema = UserActivateSchema()
