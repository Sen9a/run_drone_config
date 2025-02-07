from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Union

from urllib3.fields import RequestField

from src.const import TimeParams, ExpressLRSWifi, ExpressLRSURL
from src.dataclasess import BindingPhrase
from src.service import WifiConfig
from src.service.http_service import HttpService
import requests
from pathlib import Path
import urllib3

@dataclass
class WifiSearch:
    service: 'WifiConfig'
    http_service: 'HttpService'
    current_wifi_name: str
    current_wifi_password: str
    rx_file_path: str
    wifi_name: Union['ExpressLRSWifi'] = ExpressLRSWifi
    search_for_wifi_time: float = TimeParams.SEARCH_FOR_WIFI

    def search_wifi(self):
        current_time = datetime.utcnow()
        while (datetime.utcnow() - current_time).seconds < self.search_for_wifi_time:
            wifi_list = self.service.search_available_wifi()
            wifi = next((i for i in wifi_list if i.ssid == self.wifi_name.name), None)
            if wifi:
                return wifi

    def run(self):
        wifi_profile = self.search_wifi()
        if wifi_profile:
            self.service.connect_to_wifi(wifi_profile.ssid, self.wifi_name.password)
        else:
            print(f"Did not find wifi {self.wifi_name}")
        self.try_the_request()
        # self.http_service.post(ExpressLRSURL.config, {"json": asdict(BindingPhrase())})
        # file_path = Path(self.rx_file_path)
        # size = str(file_path.stat().st_size).encode("utf-8")
        # headers = {
        #     "Accept": "*/*",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,uk;q=0.7",
        #     "Connection": "keep-alive",
        #     "Content-Length": "1103824",
        #     "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryS13MZajeYoF6OG3e",
        #     "Host": "10.0.0.1",
        #     "Origin": "http://10.0.0.1",
        #     "Referer": "http://10.0.0.1/",
        #     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        #     "X-FileSize": "1103600"
        # }
        # with open(self.rx_file_path, "rb") as rx_file:
        #     file_data = rx_file.read()
        # fields = []
        # request_field = RequestField(name='file', data=file_data, filename=file_path.name)
        # content_disposition = f'form-data; size={len(file_data)}'
        # request_field.make_multipart(content_disposition=content_disposition, content_type='multipart/form-data')
        # fields.append(request_field)
        # data = self.http_service.post_http(ExpressLRSURL.update, {"fields": fields}, headers)
        # if data.get("status") == 'mismatch':
        #     payload = {'action': data.get('msg')}
        #     data = self.http_service.post(ExpressLRSURL.forceupdate, {"json": payload})
        #     if data.get("status") == 'ok':
        #         data = self.http_service.post(ExpressLRSURL.reboot, {"json": {}})
        self.service.connect_to_wifi(self.current_wifi_name, self.current_wifi_password)

    def read_file_in_chunks(self, chunk_size=10):
        """Generator to read a file in chunks."""
        with open(self.rx_file_path, "rb") as file:
            while chunk := file.read(chunk_size):
                yield chunk

    def try_the_request(self):

        url = "http://10.0.0.1/update?force"

        payload = {'file_name': 'HappyModel_ES900_Dual_RX_ESP32.bin'}
        files = {
            'upload': ('HappyModel_ES900_Dual_RX_ESP32.bin',
                       open('/home/sen9a/drones/Rusorizu/ELRS/HappyModel_ES900_Dual_RX_ESP32.bin', 'rb'),
                       'application/gzip',
                       None)
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,uk;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '1103824',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryoMSbkftHZEpmtVeY',
            'Host': '10.0.0.1',
            'Origin': 'http://10.0.0.1',
            'Referer': 'http://10.0.0.1/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'X-FileSize': '1103600'
        }

        response = requests.post(url, headers=headers, data=payload, files=files)
        print(response.text)
