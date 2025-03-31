from typing import Optional

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    usb_port: str = '/dev/ttyACM0'
    baudrate: int = 115200
    read_wait_max: int = 5
    timeout: int = 30
    wifi_password: Optional[str] = None
    wifi_ssid: Optional[str] = None
    current_wifi: Optional[str] = None
    current_wifi_password: Optional[str] = None
    bind_value: Optional[str] = None

    class Config:
        env_file = '.env'


setting = Settings()