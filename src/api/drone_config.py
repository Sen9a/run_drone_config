from typing import Optional

from fastapi import APIRouter, File, UploadFile

from src.client.betaflight import BetaFlightClient
from src.client.wifi_configs import WifiConfigClient
from src.const import ExpressLRSURL
from src.managers import WriteCli, WifiSearch
from src.schemas import ConfigResponse
from src.schemas.general_response import GeneralResponse
from src.service import BetaFlight, WifiConfig
from src.service.firmware_service import FirmwareService
from src.service.http_service import HttpService
from src.settings import setting

router = APIRouter(prefix="/configs")


@router.post("/", response_model=GeneralResponse)
def post_config(beta_flight_config: Optional[UploadFile] = File(None),
                beta_flight_firmware: Optional[UploadFile] = File(None),
                rx_config: Optional[UploadFile] = File(None)):
    response = GeneralResponse(beta_flight_config=ConfigResponse(status='Not Processed',
                                                                 message='No config file provided'),
                               rx_config=ConfigResponse(status='Not Processed',
                                                        message='No config file provided'))
    if {beta_flight_config, rx_config, beta_flight_firmware} == {None}:
        config_response = ConfigResponse(status='Error', message='No config file provided')
        return config_response
    else:
        if beta_flight_firmware:
            a = FirmwareService()
            a.run_firmware(beta_flight_firmware)
        if beta_flight_config:
            service = BetaFlight(setting.port)
            client = BetaFlightClient(service)
            manager = WriteCli(client)
            response.beta_flight_config = ConfigResponse(**manager.run(beta_flight_config))
        if rx_config:
            wifi_service = WifiConfig()
            http_service = HttpService(ExpressLRSURL.URL)
            client = WifiConfigClient(wifi_service, http_service)
            wifi_manager = WifiSearch(client,
                                      setting.current_wifi,
                                      setting.current_wifi_password)
            response.rx_config = ConfigResponse(**wifi_manager.run(rx_config))
        return response
