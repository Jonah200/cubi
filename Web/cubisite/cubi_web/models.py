import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
import paho.mqtt.publish
import json


def generate_association_code() -> str:
    return uuid.uuid4().hex

class User(AbstractUser):
    role = models.CharField(max_length=32, default='user')
    created_at = models.DateTimeField(auto_now_add=True)


class Device(models.Model):
    device_id = models.CharField(max_length=255, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=255, blank=True, default='')
    association_code = models.CharField(
        max_length=32, unique=True, default=generate_association_code,
    )

    def _generate_device_association_topic(self) -> str:
        return 'devices/{}/cubi/associated'.format(self.device_id)

    def publish_unassociated_message(self) -> None:
        assoc_msg = {}
        assoc_msg['associated'] = False
        assoc_msg['code'] = self.association_code
        paho.mqtt.publish.single(
            self._generate_device_association_topic(),
            json.dumps(assoc_msg),
            qos=2,
            retain=True,
            hostname="localhost",
            port=50001
        )

    def associate_and_publish_associated_msg(self, user: User) -> None:
        self.owner = user
        self.save()
        assoc_msg = {}
        assoc_msg['associated'] = True
        assoc_msg['username'] = self.owner.username
        paho.mqtt.publish.single(
            self._generate_device_association_topic(),
            json.dumps(assoc_msg),
            qos=2,
            retain=True,
            hostname="localhost",
            port=50001
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
