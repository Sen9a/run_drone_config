from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.service.firmware_service import FirmwareService
    from tempfile import NamedTemporaryFile


@dataclass
class FirmwareClient:
    service: 'FirmwareService'

    def execute_list_dfu(self):
        return self.service.execute_list_dfu()

    def execute_dfu_update(self, file: 'NamedTemporaryFile'):
        return self.service.execute_dfu_update(file.name)

    def crate_intel_obj(self, source_file: 'NamedTemporaryFile', target_file: 'NamedTemporaryFile'):
        return self.service.crate_intel_obj(source_file, target_file)

