from typing import Any, Dict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from subscription.models import (
    UserSubscription,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    device_id = serializers.CharField(required=False)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        if 'email' in attrs and not attrs['email'].islower():
            raise ValidationError('Email should be lowercase')
        data = super().validate(attrs)
        data['id'] = self.user.pk
        data['user_device_id'] = self.user.device_id
        data['device_id'] = attrs.get("device_id", None)
        return data
