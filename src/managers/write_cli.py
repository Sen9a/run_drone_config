from dataclasses import dataclass
from typing import Optional

from src.client.betaflight import BetaFlightClient
from src.const import ErrorString


@dataclass
class WriteCli:
    betaflight_client: BetaFlightClient
    file_source: Optional[str] = None


    def run(self):
        if self.file_source:
            with open(self.file_source, "r") as file:
                with self.betaflight_client.connect() as client:
                    with client.cli_mode():
                        response = client.read_response()
                        print(response)
                        for line in file:
                            if not line.startswith("#") and line.strip("\n"):
                                print("-" * 100)
                                client.execute(line)
                                response = client.read_response()
                                if ErrorString.ERROR_IN_SAVE in response:
                                    client.send_save_command()
