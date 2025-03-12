import subprocess
from dataclasses import dataclass

from intelhex import IntelHex
import tempfile

@dataclass
class FirmwareService:

    @staticmethod
    def execute_list_dfu():
        return subprocess.run(["dfu-util", "--list"], capture_output=True, text=True)

    @staticmethod
    def execute_dfu_update(file: tempfile.NamedTemporaryFile):
        return  subprocess.run(['dfu-util', '-d', '0483:df11', '-D', file.name,
                                     '--alt', '0', '-s', '0x08000000:mass-erase:force:leave', '--reset'],
                                     capture_output=True, text=True)

    @staticmethod
    def crate_intel_obj(source_file: tempfile.NamedTemporaryFile, target_file: tempfile.NamedTemporaryFile):
        intel = IntelHex(source_file.name)
        intel.tobinfile(target_file)
