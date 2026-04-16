import json
import re
import uuid
from datetime import timedelta

import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand

from cubi_web.models import Device, Solve, User

MQTT_BROKER_RE_PATTERN: str = (r'\$sys\/broker\/connection\/'
                               r'(?P<device_id>[0-9a-f]*)_cubi_broker/state')

class Command(BaseCommand):
    help = 'Long-running MQTT daemon for device discovery and association'

    def handle(self, *args, **options):
        self.parked_user, _ = User.objects.get_or_create(
            username='parked_device_user',
            defaults={'is_active': False},
        )

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = self._on_connect
        client.user_data_set({'client': client})

        self.stdout.write(f'Connecting to MQTT broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}')
        client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT)
        client.loop_forever()

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        self.stdout.write(f'Connected to MQTT broker (rc={reason_code})')
        client.message_callback_add('$SYS/broker/connection/+/state',
                                         self._handle_device_connection)
        client.subscribe('$SYS/broker/connection/+/state')
        self.client.message_callback_add('devices/+/cubi/solve',
                                         self._handle_solve)
        client.subscribe('cubi/solve')

    def _handle_solve(self, msg):
        try:
            data = json.loads(msg.payload.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.stderr.write('Invalid solve payload')
            return

        device_id = data.get('device_id')
        scramble = data.get('scramble')
        solve_time = data.get('solve_time')

        if not all([device_id, scramble, solve_time is not None]):
            self.stderr.write('Missing required fields in solve payload')
            return

        try:
            device = Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            self.stderr.write(f'Unknown device: {device_id}')
            return

        if device.owner == self.parked_user:
            self.stderr.write(f'Device not associated: {device_id}')
            return

        solve = Solve.objects.create(
            user=device.owner,
            scramble=scramble,
            solve_time=timedelta(seconds=float(solve_time)),
        )
        self.stdout.write(f'Saved {solve}')

    def _handle_device_connection(self, client, msg):
        # Topic: $SYS/broker/connection/<device_id>/state
        if msg.payload == b'1':
            results = re.search(MQTT_BROKER_RE_PATTERN, msg.topic.lower())
            if results is None:
                return 
            device_id = results.group('device_id')
            try:
                device = Device.objects.get(device_id=device_id)
                print("Found {}".format(device))
            except Device.DoesNotExist:
                new_device = Device(device_id=device_id)
                uname = settings.DEFAULT_USER
                new_device.owner = User.objects.get(username=uname)
                new_device.save()
                print("Created {}".format(new_device))
                new_device.publish_unassociated_message()
