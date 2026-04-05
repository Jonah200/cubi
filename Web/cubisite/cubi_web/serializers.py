from rest_framework import serializers

from .models import Device


class AssociateDeviceSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=32)

    def validate_code(self, value):
        try:
            device = Device.objects.get(association_code=value.upper())
        except Device.DoesNotExist:
            raise serializers.ValidationError('Invalid association code.')
        self._device = device
        return value
