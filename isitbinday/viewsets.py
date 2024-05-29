# Third Party
from rest_framework import viewsets


class OwnedModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return super().get_queryset().authorize(self.request, action="retrieve")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
