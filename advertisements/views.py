from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from advertisements.filters import AdvertisementFilter
from django_filters import rest_framework as filters

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from api_with_restrictions.permissions import IsOwnerPermission


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    permission_classes = [IsAuthenticated,IsOwnerPermission]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        return super().perform_create(serializer)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

    def perform_update(self, serializer):
        serializer.save(creator=self.request.user)
        return super().perform_update(serializer)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['create', 'update', 'partial_update','destroy']:
            return [IsAuthenticated(),IsOwnerPermission()]
        return []
