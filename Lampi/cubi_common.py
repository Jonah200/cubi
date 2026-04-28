BROKER_HOST = 'localhost'
BROKER_PORT = 1883

DEVICE_ID_FILENAME = '/sys/class/net/eth0/address'

def get_device_id() -> str:
    mac_addr = open(DEVICE_ID_FILENAME).read().strip()
    return mac_addr.replace(":", "")