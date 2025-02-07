from typing import Optional

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: str = '/dev/ttyUSB0'
    baudrate: int = 115200
    read_wait_max: int = 5
    timeout: int = 30
    wifi_password: Optional[str] = None
    wifi_ssid: Optional[str] = None

    class Config:
        env_file = '.env'


setting = Settings()