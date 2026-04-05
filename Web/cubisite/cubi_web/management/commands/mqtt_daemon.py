import json
import uuid

import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand

from cubi_web.models import Device, User


class Command(BaseCommand):
    help = 'Long-running MQTT daemon for device discovery and association'

    def handle(self, *args, **options):
        self.parked_user, _ = User.objects.get_or_create(
            username='parked_device_user',
            defaults={'is_active': False},
        )

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.user_data_set({'client': client})

        self.stdout.write(f'Connecting to MQTT broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}')
        client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT)
        client.loop_forever()

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        self.stdout.write(f'Connected to MQTT broker (rc={reason_code})')
        client.subscribe('$SYS/broker/connection/+/state')

    def _on_message(self, client, userdata, msg):
        # Topic: $SYS/broker/connection/<device_id>/state
        parts = msg.topic.split('/')
        if len(parts) != 5:
            return

        device_id = parts[3]
        payload = msg.payload.decode().strip()

        if payload != '1':
            return

        try:
            device = Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            device = None

        if device is None:
            # New device — create with association code
            code = uuid.uuid4().hex[:6].upper()
            device = Device.objects.create(
                device_id=device_id,
                owner=self.parked_user,
                association_code=code,
            )
            self.stdout.write(f'New device discovered: {device_id}, code={code}')
            client.publish(
                f'cubi/{device_id}/associated',
                payload=json.dumps({'code': code, 'associated': False}),
                retain=True,
            )
        elif device.owner == self.parked_user:
            # Device exists but still parked — re-publish existing code
            self.stdout.write(f'Re-publishing code for parked device: {device_id}')
            client.publish(
                f'cubi/{device_id}/associated',
                payload=json.dumps({'code': device.association_code, 'associated': False}),
                retain=True,
            )
        else:
            # Device already associated
            self.stdout.write(f'Device already associated: {device_id}')
            client.publish(
                f'cubi/{device_id}/associated',
                payload=json.dumps({'associated': True}),
                retain=True,
            )
