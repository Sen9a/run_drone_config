from dataclasses import dataclass
from datetime import datetime

from src.const import TimeParams, WifiNames
from src.service import WifiConfig


@dataclass
class WifiSearch:
    service: 'WifiConfig'
    wifi_name: str = WifiNames.ExpressLRS
    search_for_wifi_time: float = TimeParams.SEARCH_FOR_WIFI

    def search_wifi(self):
        current_time = datetime.utcnow()
        while (datetime.utcnow() - current_time).seconds < self.search_for_wifi_time:
            wifi_list = self.service.search_available_wifi()
            wifi = next((i for i in wifi_list if i.ssid == self.wifi_name), None)
            if wifi:
                return wifi

    def run(self):
        wifi_profile = self.search_wifi()
        if not wifi_profile:
            print(f"Did not find wifi {self.wifi_name}")
        self.service.connect_to_wifi(wifi_profile.ssid, wifi_profile.key)
