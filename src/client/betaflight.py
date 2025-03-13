from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generator, Any
import time

from src.const import Commands

if TYPE_CHECKING:
    from src.service import BetaFlight

@dataclass
class BetaFlightClient:
    service: 'BetaFlight'

    @contextmanager
    def connect(self) -> Generator['BetaFlightClient', None, None]:
        try:
            with self.service.connect() as conn:
                print(f"the port connection name {conn.connection.name}")
                yield self
        except Exception as e:
            print(f'Error occurred while connecting to {self.service.port} error: {e}')
            raise e

    @contextmanager
    def cli_mode(self) -> Generator[None, Any, None]:
        try:
            self.service.execute_command(Commands.START_CLI)
            print("Enter cli mode")
            yield
        finally:
            print("Exit cli mode")

    def execute(self, command):
        return self.service.execute_command(command)

    def read_response(self):
        return self.service.read_response()

    def send_save_command(self):
        return self.service.execute_command(Commands.SAVE)
