import json
import queue
import threading
import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqtt_publish
from django.conf import settings
from django.contrib.auth import login, logout
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Solve, User
from .serializers import (
    AssociateDeviceSerializer,
    LoginSerializer,
    SignupSerializer,
    SolveSerializer,
)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'detail': 'CSRF cookie set'})


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
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
            'firstName': request.user.first_name,
            'lastName': request.user.last_name,
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


class SolvesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        solves = Solve.objects.filter(user=request.user).order_by('-created_at')
        serializer = SolveSerializer(solves, many=True)
        return Response(serializer.data)


class StatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        solves = list(
            Solve.objects.filter(user=request.user)
            .order_by('-created_at')
            .values_list('solve_time', flat=True)
        )
        times = [s.total_seconds() for s in solves]

        def avg(lst):
            return sum(lst) / len(lst) if lst else None

        def best_ao(times, n):
            if len(times) < n:
                return None
            best = None
            for i in range(len(times) - n + 1):
                window = times[i : i + n]
                a = avg(window)
                if best is None or a < best:
                    best = a
            return round(best, 2) if best is not None else None

        return Response({
            'mostRecent': round(times[0], 2) if times else None,
            'averageOf5': round(avg(times[:5]), 2) if len(times) >= 5 else None,
            'averageOf10': round(avg(times[:10]), 2) if len(times) >= 10 else None,
            'bestSingle': round(min(times), 2) if times else None,
            'bestAo5': best_ao(times, 5),
            'bestAo10': best_ao(times, 10),
            'bestAo50': best_ao(times, 50),
        })


class ServerSentEventRenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class SolvesStreamView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [ServerSentEventRenderer]

    def get(self, request):
        user = request.user
        device_ids = set(
            user.devices.values_list('device_id', flat=True)
        )

        q = queue.Queue()

        def on_connect(client, userdata, flags, reason_code, properties):
            client.subscribe('cubi/solve')

        def on_message(client, userdata, msg):
            try:
                data = json.loads(msg.payload.decode())
            except (json.JSONDecodeError, UnicodeDecodeError):
                return
            if data.get('device_id') in device_ids:
                q.put(data)

        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT)
        mqtt_client.loop_start()

        def event_stream():
            try:
                while True:
                    try:
                        data = q.get(timeout=15)
                    except queue.Empty:
                        yield ': ping\n\n'
                        continue

                    solve = (
                        Solve.objects.filter(user=user)
                        .order_by('-created_at')
                        .first()
                    )
                    if solve:
                        serialized = SolveSerializer(solve).data
                        yield f'event: solve\ndata: {json.dumps(serialized)}\n\n'
            finally:
                mqtt_client.loop_stop()
                mqtt_client.disconnect()

        response = StreamingHttpResponse(
            event_stream(), content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response
