from pydantic import BaseModel

from src.schemas import ConfigResponse


class GeneralResponse(BaseModel):
    beta_flight_config: ConfigResponse
    rx_config: ConfigResponse
    beta_flight_firmware: ConfigResponse
