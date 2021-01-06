# Third Party
from rest_framework import permissions, viewsets
from rest_framework.response import Response

# Locals
from .models import HomeGroup
from .permissions import IsOwner
from .serializers import HomeGroupSerializer, UserSerializer


# class UserProfileViewSet(viewsets.ViewSetMixin, generics.GenericAPIView):
class UserProfileViewSet(viewsets.ViewSet):
    """
    API endpoint for the current user
    """

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, format=None):
        serializer = UserSerializer(request.user, many=False)

        return Response(serializer.data)


class HomeGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint for home groups
    """

    serializer_class = HomeGroupSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all tasks for the currently authenticated user.
        """

        return HomeGroup.objects.authorize(self.request, action="retrieve")
