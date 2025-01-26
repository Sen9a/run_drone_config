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

    def connect_to_wifi(self, name: str, password: str):
        self.interface.disconnect()
        profile = pywifi.Profile()
        profile.ssid = name
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        if password:
            profile.key = password
        profile = self.interface.add_network_profile(profile)
        self.interface.connect(profile)

