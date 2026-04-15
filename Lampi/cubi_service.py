#!/usr/bin/env python3
import json
import socket
import time

import paho.mqtt.client as mqtt

BROKER_HOST = 'localhost'
BROKER_PORT = 1883


class CubiService:
    def __init__(self) -> None:
        self.device_id = socket.gethostname()

        self._client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=self.device_id,
        )
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

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

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        client.subscribe(f'cubi/{self.device_id}/associated')

    def _on_message(self, client, userdata, msg):
        # Association handling to be integrated later
        pass
