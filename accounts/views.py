# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Third Party
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Locals
from .serializers import AcctivateSerializer, GoogleJWTLoginSerializer, UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserActivate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AcctivateSerializer
    permission_classes = (AllowAny,)


class GoogleJWTLogin(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GoogleJWTLoginSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                audience=settings.GOOGLE_OAUTH_CLIENT_ID,
            )
            email = idinfo["email"]
            first_name = idinfo.get("given_name", "")
            last_name = idinfo.get("family_name", "")
        except Exception as e:
            return Response({"error": f"Invalid token: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        user_model = get_user_model()
        try:
            if not email.endswith("@gmail.com"):
                raise user_model.DoesNotExist
            user = user_model.objects.get(email=email.replace("@gmail.com", "@googlemail.com"))
            created = False
        except user_model.DoesNotExist:
            user, created = user_model.objects.get_or_create(
                email=email,
                defaults={
                    "username": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_active": True,
                },
            )

        if not user.is_active:
            user.is_active = True
            user.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
