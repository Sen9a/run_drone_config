from dataclasses import dataclass
from typing import Dict, Any

from fastapi import UploadFile

from src.client.betaflight import BetaFlightClient
from src.const import ErrorString


@dataclass
class WriteCli:
    beta_flight_client: BetaFlightClient


    def run(self, file: UploadFile) -> Dict[str, Any]:
        if file:
            try:
                with self.beta_flight_client.connect() as client:
                    with client.cli_mode():
                        response = client.read_response()
                        print(response)
                        for line in file.file:
                            file_line = line.decode('utf-8')
                            if not file_line.startswith("#") and (file_line := file_line.strip()):
                                print("-" * 100)
                                client.execute(file_line)
                                response = client.read_response()
                                if ErrorString.ERROR_IN_SAVE in response:
                                    client.send_save_command()
            except Exception as e:
                return {'status':'Error', 'message': str(e)}
        return {'status':'Success', 'message': 'Config saved successfully'}
