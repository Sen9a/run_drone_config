import tempfile
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.client import FirmwareClient
from src.const import Commands, DFU

if TYPE_CHECKING:
    from fastapi import UploadFile
    from src.client.betaflight import BetaFlightClient


@dataclass
class FirmwareManager:
    client: 'FirmwareClient'
    beta_flight_client: 'BetaFlightClient'
    file: 'UploadFile'

    def run(self):
        result = {'status': 'Success', 'message': 'config updated'}
        try:
            with self.beta_flight_client.connect() as client:
                with client.cli_mode():
                    response = client.read_response()
                    print(response)
                    client.execute(Commands.FIRMWARE_UPDATE)
                    with tempfile.TemporaryDirectory() as tmp_directory:
                        hex_file = tempfile.NamedTemporaryFile(dir=tmp_directory, suffix='.hex', delete=False)
                        bin_file = tempfile.NamedTemporaryFile(dir=tmp_directory, suffix='.bin', delete=False)
                        with open(hex_file.name, 'w') as write_hex_file:
                            write_hex_file.write(self.file.file.read().decode('utf-8'))
                        self.client.crate_intel_obj(hex_file, bin_file)
                        dfu_list = self.client.execute_list_dfu()
                        if DFU.check_str in dfu_list.stdout:
                            flush_result = self.client.execute_dfu_update(bin_file)
                            print(flush_result.stdout)
                            print(flush_result.stderr)
            time.sleep(15)
        except Exception as e:
            result['status'] = 'Error'
            result['message'] = str(e)
        return result

