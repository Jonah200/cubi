from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Device, Solve, User


class SolveSerializer(serializers.ModelSerializer):
    solveNo = serializers.SerializerMethodField()
    solveTime = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Solve
        fields = ['solveNo', 'solveTime', 'createdAt', 'scramble']

    def get_solveNo(self, obj):
        return Solve.objects.filter(
            user=obj.user, created_at__lte=obj.created_at
        ).count()

    def get_solveTime(self, obj):
        return obj.solve_time.total_seconds()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, default='')
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already taken.')
        return value

    def validate_password(self, value):
        validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')
        attrs['user'] = user
        return attrs


class AssociateDeviceSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=32)

    def validate_code(self, value):
        upper = value.upper()
        try:
            device = Device.objects.get(association_code__startswith=upper)
        except (Device.DoesNotExist, Device.MultipleObjectsReturned):
            raise serializers.ValidationError('Invalid association code.')
        self._device = device
        return value
