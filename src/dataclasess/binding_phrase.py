from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class BindingPhrase:
    serial_protocol: int = 0
    serial1_protocol: int = 0
    sbus_failsafe: int = 0
    modelid: int = 0
    force_tlm: int = 0
    vbind: int = 0
    uid: List[int] = field(default_factory=lambda: [6, 213, 167, 188, 3, 52])
    pwm: List[Any] = field(default_factory=list)
