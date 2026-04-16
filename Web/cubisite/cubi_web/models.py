from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField(max_length=32, default='user')
    created_at = models.DateTimeField(auto_now_add=True)


class Device(models.Model):
    device_id = models.CharField(max_length=255, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=255, blank=True, default='')
    association_code = models.CharField(
        max_length=32, unique=True, null=True, blank=True,
    )

    def __str__(self):
        return self.device_id


class Solve(models.Model):
    solve_no = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solves')
    scramble = models.TextField()
    solve_time = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Solve #{self.solve_no} — {self.solve_time}'
