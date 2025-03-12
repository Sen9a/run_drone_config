from dataclasses import dataclass
from typing import Dict, Any, TYPE_CHECKING

from fastapi import UploadFile
from src.const import ErrorString

if TYPE_CHECKING:
    from src.client.betaflight import BetaFlightClient



@dataclass
class WriteCli:
    beta_flight_client: 'BetaFlightClient'


    def run(self, file: UploadFile) -> Dict[str, Any]:
        result = {'status':'Success', 'message': 'Config saved successfully'}
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
            result['status'] = 'Error'
            result['message'] = str(e)
        return result
