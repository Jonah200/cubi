from django.conf import settings
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django_eventstream import send_event
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
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
            'hasDevice': request.user.devices.exists(),
        })


class AssociateDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AssociateDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device = serializer._device
        device.associate_and_publish_associated_msg(request.user)
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


@method_decorator(csrf_exempt, name='dispatch')
class NotifySolveView(View):
    """Internal endpoint called by mqtt_daemon to push SSE events.
    Restricted to localhost and authenticated via shared secret."""

    def post(self, request):
        remote = request.META.get('REMOTE_ADDR', '')
        if remote not in ('127.0.0.1', '::1'):
            return JsonResponse({'error': 'forbidden'}, status=403)

        token = request.headers.get('Authorization', '')
        if token != f'Bearer {settings.INTERNAL_API_SECRET}':
            return JsonResponse({'error': 'unauthorized'}, status=401)

        solve_pk = request.POST.get('solve_pk')
        if not solve_pk:
            return JsonResponse({'error': 'missing solve_pk'}, status=400)

        try:
            solve = Solve.objects.select_related('user').get(pk=solve_pk)
        except Solve.DoesNotExist:
            return JsonResponse({'error': 'not found'}, status=404)

        send_event(
            f'user-{solve.user.pk}',
            'solve',
            SolveSerializer(solve).data,
        )
        return JsonResponse({'ok': True})


