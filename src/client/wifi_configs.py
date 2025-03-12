from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Any, Tuple

if TYPE_CHECKING:
    from src.service import WifiConfig
    from src.service.http_service import HttpService

@dataclass
class WifiConfigClient:
    wifi_config: 'WifiConfig'
    http_service: 'HttpService'

    def search_available_wifi(self):
        return self.wifi_config.search_available_wifi()

    def connect_to_wifi(self, ssid: str, password: str):
        return self.wifi_config.connect_to_wifi(ssid, password)

    def http_post(self, url: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> Tuple[int, Dict[str, Any]]:
        return self.http_service.post(url, data, headers)