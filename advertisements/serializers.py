from os import stat
from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.context['request'].method == 'POST':
            if len(list(Advertisement.objects.filter(status='OPEN'))) >= 10:
                raise serializers.ValidationError('Нельзя создавать больше 10 объявлений.')
        
        if self.context['request'].method == 'PATCH':
            if self.context['request'].data['status'] != 'CLOSED':
                if len(list(Advertisement.objects.filter(status='OPEN'))) >= 10:
                    raise serializers.ValidationError('Открытых объявлений больше 10, нельзя снова открыть это объявление')
        return data
