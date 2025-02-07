from typing import Optional

from fastapi import APIRouter, File, UploadFile

from src.client.betaflight import BetaFlightClient
from src.managers import WriteCli
from src.schemas import ConfigResponse
from src.service import BetaFlight
from src.settings import setting

router = APIRouter(prefix="/configs")


@router.post("/", response_model=ConfigResponse)
def post_config(beta_flight_config: Optional[UploadFile] = File(None),
                rx_config: Optional[UploadFile] = File(None),
                tx_config: Optional[UploadFile] = File(None)):
    if {beta_flight_config, rx_config, tx_config} == {None}:
        config_response = ConfigResponse(status='Error', message='No config file provided')
        return config_response, 402
    else:
        service = BetaFlight(setting.PORT)
        client = BetaFlightClient(service)
        manager = WriteCli(client, beta_flight_config)
        manager.run()