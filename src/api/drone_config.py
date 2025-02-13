from typing import Optional

from fastapi import APIRouter, File, UploadFile

from src.client.betaflight import BetaFlightClient
from src.const import ExpressLRSURL
from src.managers import WriteCli, WifiSearch
from src.schemas import ConfigResponse
from src.schemas.general_response import GeneralResponse
from src.service import BetaFlight, WifiConfig
from src.service.http_service import HttpService
from src.settings import setting

router = APIRouter(prefix="/configs")


@router.post("/", response_model=GeneralResponse)
def post_config(beta_flight_config: Optional[UploadFile] = File(None),
                rx_config: Optional[UploadFile] = File(None),
                tx_config: Optional[UploadFile] = File(None)):
    response = GeneralResponse(beta_flight_config=ConfigResponse(status='Not Processed',
                                                                 message='No config file provided'),
                               rx_config=ConfigResponse(status='Not Processed',
                                                        message='No config file provided'))
    if {beta_flight_config, rx_config, tx_config} == {None}:
        config_response = ConfigResponse(status='Error', message='No config file provided')
        return config_response
    else:
        if beta_flight_config:
            service = BetaFlight(setting.port)
            client = BetaFlightClient(service)
            manager = WriteCli(client)
            response.beta_flight_config = ConfigResponse(**manager.run(beta_flight_config))
        if rx_config:
            wifi_service = WifiConfig()
            http_service = HttpService(ExpressLRSURL.URL)
            wifi_manager = WifiSearch(wifi_service,
                                      http_service,
                                      setting.current_wifi,
                                      setting.current_wifi_password)
            response.rx_config = ConfigResponse(**wifi_manager.run(rx_config))
        return response
