import json

import paho.mqtt.publish as mqtt_publish
from django.conf import settings
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import AssociateDeviceSerializer, LoginSerializer, SignupSerializer


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            password=serializer.validated_data['password'],
        )
        login(request, user)
        return Response(
            {'id': user.id, 'username': user.username},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'id': user.id, 'username': user.username})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        })


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
