import time
from dataclasses import dataclass, asdict
from datetime import datetime
from http.client import HTTPException
from typing import Union

from fastapi import UploadFile
import requests

from src.const import TimeParams, ExpressLRSWifi, ExpressLRSURL
from src.dataclasess import BindingPhrase
from src.service import WifiConfig
from src.service.http_service import HttpService


@dataclass
class WifiSearch:
    service: 'WifiConfig'
    http_service: 'HttpService'
    current_wifi_name: str
    current_wifi_password: str
    wifi_name: Union['ExpressLRSWifi'] = ExpressLRSWifi
    search_for_wifi_time: float = TimeParams.SEARCH_FOR_WIFI

    def search_wifi(self):
        current_time = datetime.utcnow()
        while (datetime.utcnow() - current_time).seconds < self.search_for_wifi_time:
            wifi_list = self.service.search_available_wifi()
            wifi = next((i for i in wifi_list if i.ssid == self.wifi_name.name), None)
            if wifi:
                return wifi

    def run(self, file: UploadFile):
        result = {'status': 'Success', 'message': 'config updated'}
        try:
            self.update_firmware(file)
            print(f'Waiting until reload for {TimeParams.WAIT_UNTIL_RELOAD}')
            time.sleep(TimeParams.WAIT_UNTIL_RELOAD)
            self.update_bind_phrase()
        except HTTPException as e:
            result["status"] = "Error"
            result["message"] = str(e)
        self.service.connect_to_wifi(self.current_wifi_name, self.current_wifi_password)
        return result

    def update_firmware(self, file: UploadFile):
        wifi_profile = self.search_wifi()
        if wifi_profile:
            self.service.connect_to_wifi(wifi_profile.ssid, self.wifi_name.password)
            self.send_config(file)
        else:
            print(f"Did not find wifi {self.wifi_name}")

    def update_bind_phrase(self):
        wifi_profile = self.search_wifi()
        if wifi_profile:
            self.service.connect_to_wifi(wifi_profile.ssid, self.wifi_name.password)
            time.sleep(3)
            self.http_service.post(ExpressLRSURL.config, json=asdict(BindingPhrase()))
            self.service.connect_to_wifi(self.current_wifi_name, self.current_wifi_password)

    def send_config(self, file: UploadFile):
        file.file.seek(0, 2)  # Seek to the end of the file
        file_size = file.file.tell()  # Get the file size in bytes
        file.file.seek(0)  #
        files = {'upload': (file.filename, file.file.read(), file.content_type)}
        headers = {
            "X-FileSize": str(file_size)
        }
        response = {'response': 'test'}
        try:
            _, response = self.http_service.post(ExpressLRSURL.update,
                                                 files=files,
                                                 headers=headers,
                                                 timeout=60)
        except requests.exceptions.ReadTimeout:
            print("ELRS doesn't send response")
        return response
