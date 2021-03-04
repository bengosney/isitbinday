# Django
from django.contrib.auth.models import User

# Third Party
from rest_framework import generics
from rest_framework.permissions import AllowAny

# Locals
from .serializers import UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
