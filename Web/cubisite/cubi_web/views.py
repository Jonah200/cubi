import json

import paho.mqtt.publish as mqtt_publish
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AssociateDeviceSerializer


class AssociateDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AssociateDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device = serializer._device
        device.owner = request.user
        device.association_code = None
        device.save()

        mqtt_publish.single(
            topic=f'cubi/{device.device_id}/associated',
            payload=json.dumps({'associated': True}),
            hostname=settings.MQTT_BROKER_HOST,
            port=settings.MQTT_BROKER_PORT,
            retain=True,
        )

        return Response(
            {'device_id': device.device_id, 'device_name': device.device_name},
            status=status.HTTP_200_OK,
        )
