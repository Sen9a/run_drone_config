from dataclasses import dataclass, field
from typing import List, Any

import settings
from src.settings import setting


@dataclass
class BindingPhrase:
    serial_protocol: int = 0
    serial1_protocol: int = 0
    sbus_failsafe: int = 0
    modelid: int = 0
    force_tlm: int = 0
    vbind: int = 0
    uid: List[int] = field(default_factory=lambda: setting.bind_value.split(','))
    pwm: List[Any] = field(default_factory=list)
