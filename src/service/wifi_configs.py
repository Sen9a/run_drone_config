import subprocess
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import pywifi

if TYPE_CHECKING:
    from pywifi import PyWiFi
    from pywifi.iface import Interface


@dataclass
class WifiConfig:
    wifi: 'PyWiFi' = pywifi.PyWiFi()
    interface: Optional['Interface'] = None

    @property
    def get_interface(self) -> 'Interface':
        if self.interface is None:
            self.interface = next(iter(self.wifi.interfaces()), None)
        return self.interface

    def search_available_wifi(self):
        self.get_interface.scan()
        print("Scanning wifi please wait...")
        time.sleep(3)
        return self.interface.scan_results()

    def disconnect_wifi(self):
        self.get_interface.disconnect()

    @staticmethod
    def connect_to_wifi(name: str, password: str):
        try:
            subprocess.run(["nmcli", "dev", "wifi", "connect", name, "password", password], check=True)
            print(f"Connected to {name} successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

