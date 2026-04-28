#!/usr/bin/env python3
import json
import socket
import time

import paho.mqtt.client as mqtt

from cubi_common import *

class CubiService:
    def __init__(self) -> None:
        self.device_id = get_device_id()

        self._client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=self.device_id,
        )
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

    def start(self) -> None:
        self._client.connect_async(BROKER_HOST, BROKER_PORT)
        self._client.loop_start()

    def publish_solve(self, scramble: str, elapsed: float) -> None:
        payload = json.dumps({
            'device_id': self.device_id,
            'scramble': scramble,
            'solve_time': round(elapsed, 3),
            'timestamp': time.time(),
        })
        self._client.publish(f'cubi/solve', payload)

    def stop(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    # Callbacks set by the app layer.
    # on_association_required(code: str) — device is unassociated; code is the full UUID
    # on_associated(username: str)       — device has been claimed by username
    on_association_required = None
    on_associated = None

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        client.subscribe('cubi/associated')

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return

        if payload.get('associated') is False:
            code = payload.get('code', '')
            if self.on_association_required:
                self.on_association_required(code)
        elif payload.get('associated') is True:
            username = payload.get('username', '')
            if self.on_associated:
                self.on_associated(username)
