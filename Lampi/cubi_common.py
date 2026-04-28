BROKER_HOST = 'localhost'
BROKER_PORT = 1883

DEVICE_ID_FILENAME = '/sys/class/net/eth0/address'

def get_device_id() -> str:
    mac_addr = open(DEVICE_ID_FILENAME).read().strip()
    return mac_addr.replace(":", "")

COLOR_MAP = {"y": (1,1,0,1),
             "g": (0,0.87,0,1),
             "w": (1,1,1,1),
             "o": (1,0.67,0,1),
             "r": (1,0,0,1),
             "b": (0,0,1,1)
             }
