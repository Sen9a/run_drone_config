from dataclasses import dataclass
from typing import Dict, Any
from urllib import parse
from http import HTTPStatus
import requests
import urllib3


@dataclass
class HttpService:
    url: str

    @staticmethod
    def parse_response(response: requests.Response) -> Dict[str, Any]:
        if response.status_code == HTTPStatus.OK:
            try:
                data = response.json()
                print(data)
                return data
            except requests.exceptions.JSONDecodeError as e:
                print("Response is not valid JSON:", e)
                print("Response text:", response.text)

    def post(self, patch: str, body: Dict[str, Any], headers: Dict[str, Any] = None) -> Dict[str, Any]:
        url = parse.urljoin(self.url, patch)
        payload = {**body}
        if headers:
            payload = {**payload, "headers": {**headers}}
        response = requests.post(url, **payload)
        return self.parse_response(response)

    def post_http(self, patch: str, body: Dict[str, Any], headers: Dict[str, Any] = None) -> Dict[str, Any]:
        http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=30, read=60))
        url = parse.urljoin(self.url, patch)
        payload = {**body}
        if headers:
            payload = {**payload, "headers": {**headers}}
        response = http.request(
            'POST',
            url,
            **payload
        )
        print(response.data.decode('utf-8'))
        print('test')

