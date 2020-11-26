# Third Party
from rest_framework import permissions, viewsets

# Locals
from . import models, serializers


class householdViewSet(viewsets.ModelViewSet):
    """ViewSet for the household class"""

    queryset = models.household.objects.all()
    serializer_class = serializers.householdSerializer
    permission_classes = [permissions.IsAuthenticated]


class memberViewSet(viewsets.ModelViewSet):
    """ViewSet for the member class"""

    queryset = models.member.objects.all()
    serializer_class = serializers.memberSerializer
    permission_classes = [permissions.IsAuthenticated]
