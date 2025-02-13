import subprocess
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pywifi
from pywifi import const

from src.const import OSSystems

if TYPE_CHECKING:
    from pywifi import PyWiFi


@dataclass
class WifiConfig:
    wifi: 'PyWiFi' = pywifi.PyWiFi()

    def __post_init__(self):
        self.interface = next(iter(self.wifi.interfaces()), None)

    def search_available_wifi(self):
        self.interface.scan()
        print("Scanning wifi please wait...")
        time.sleep(3)
        return self.interface.scan_results()

    def disconnect_wifi(self):
        self.interface.disconnect()

    @staticmethod
    def connect_to_wifi(name: str, password: str):
        try:
            subprocess.run(["nmcli", "dev", "wifi", "connect", name, "password", password], check=True)
            print(f"Connected to {name} successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

