from dataclasses import dataclass
from http.client import HTTPException
from typing import Dict, Any, Tuple, Union
from urllib import parse
from http import HTTPStatus
import requests


@dataclass
class HttpService:
    url: str

    @staticmethod
    def parse_response(response: requests.Response) -> Union[Tuple[int, str], Tuple[int, Dict[str, Any]]]:
        try:
            data = response.json()
            print(f'JSON response: {data}')
            return response.status_code, data
        except requests.exceptions.JSONDecodeError as e:
            print("Response is not valid JSON:", e)
            print("Response text:", response.text)
            return response.status_code, response.text

    def post(self, patch: str, **kwargs) -> Union[Tuple[int, str], Tuple[int, Dict[str, Any]]]:
        url = parse.urljoin(self.url, patch)
        response = requests.post(url, **kwargs)
        status_code, data = self.parse_response(response)
        if status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.NO_CONTENT):
            return status_code, data
        else:
            raise HTTPException(data)


