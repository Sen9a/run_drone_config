from dataclasses import dataclass
from enum import Enum
from symbol import pass_stmt


class ErrorString(str, Enum):
    ERROR = "ERROR"
    ERROR_IN_SAVE = "ERROR IN save"


class Commands(str, Enum):
    START_CLI = "#"
    EXIT_CLI = "exit"
    SAVE = "save"


class OSSystems(str, Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"


class NetworkCommands(str, Enum):
    NMCLI = "nmcli"
    DEVICE = "device"
    WIFI = "wifi"
    LIST = "list"
    NAME = "name"

class TimeParams(float, Enum):
    SEARCH_FOR_WIFI = 90
    READ_WAIT_MAX = 5

class EndResponseMarkers(str, Enum):
    END_OF_BETAFLIGHT_CLI = "\n#"


class ExpressLRSWifi(str, Enum):
    name = "ExpressLRS RX"
    password = "expresslrs"

class ExpressLRSURL(str, Enum):
    URL = "http://10.0.0.1/"
    config = "config"
    update = "http://10.0.0.1//update"
    forceupdate = "forceupdate"
    reboot = "reboot"

