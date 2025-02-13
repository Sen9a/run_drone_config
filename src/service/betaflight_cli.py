from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import traceback
from src.settings import setting

import serial
from colorama import Fore, Style

from src.const import ErrorString, TimeParams, EndResponseMarkers


@dataclass
class BetaFlight:
    port: str
    baudrate: int = setting.baudrate
    bytesize: 'serial' = serial.EIGHTBITS
    parity: 'serial' = serial.PARITY_NONE
    timeout: float = setting.timeout
    connection: Optional[serial.Serial] = None
    read_wait_max_time: float = TimeParams.READ_WAIT_MAX
    read_all_string_marker: str = EndResponseMarkers.END_OF_BETAFLIGHT_CLI

    @contextmanager
    def connect(self):
        try:
            if self.connection is None:
                self.connection = serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity,
                                   timeout=self.timeout)
                yield self
        except Exception as e:
            print(e)
            raise e
        finally:
            if self.connection and self.connection.is_open:
                self.connection.close()
            print('Connection closed')


    def execute_command(self, command: str):
        if self.connection.is_open:
            try:
                print(f"Executing command:\n{command}\n")
                command = command + '\r\n'
                self.connection.write(command.encode('utf-8'))
                if self.connection.is_open:
                    self.connection.flush()
            except Exception as e:
                print(f"Connection closed, please retry, exception is: {str(e)}")

    def read_response(self):
        response = ''
        if self.connection.is_open:
            current_time = datetime.utcnow()
            try:
                while (datetime.utcnow() - current_time).seconds < self.read_wait_max_time:
                    response_btf = self.connection.read(self.connection.in_waiting).decode('utf-8').strip()
                    if response_btf.endswith(self.read_all_string_marker):
                        response += response_btf
                        print("Response block:")
                        if response and ErrorString.ERROR in response:
                            print(f"{Fore.RED}{response}{Style.RESET_ALL}")
                        else:
                            print(response)
                        return response
                    else:
                        response += response_btf
                else:
                    response += "ERROR: Time Out"
            except Exception as e:
                 print(f"Connection closed, please retry, exception is: {str(e)}")
        else:
            response += 'ERROR: Connection closed, please retry'
        return response
