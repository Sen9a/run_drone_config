from typing import Optional

from fastapi import APIRouter, File, UploadFile

from src.client import FirmwareClient
from src.client.betaflight import BetaFlightClient
from src.client.wifi_configs import WifiConfigClient
from src.const import ExpressLRSURL
from src.managers import WriteCli, WifiSearch, FirmwareManager
from src.schemas import ConfigResponse
from src.schemas.general_response import GeneralResponse
from src.service import BetaFlight, WifiConfig
from src.service import FirmwareService
from src.service.http_service import HttpService
from src.settings import setting

router = APIRouter(prefix="/configs")


@router.post("/", response_model=GeneralResponse)
def post_config(beta_flight_config: Optional[UploadFile] = File(None),
                beta_flight_firmware: Optional[UploadFile] = File(None),
                rx_config: Optional[UploadFile] = File(None)):
    response = GeneralResponse(beta_flight_firmware = ConfigResponse(status='No Processed',
                                                                     message='No config file provided'),
                               beta_flight_config=ConfigResponse(status='Not Processed',
                                                                 message='No config file provided'),
                               rx_config=ConfigResponse(status='Not Processed',
                                                        message='No config file provided'))
    if {beta_flight_config, rx_config, beta_flight_firmware} == {None}:
        config_response = ConfigResponse(status='Error', message='No config file provided')
        return config_response
    else:
        beta_flight_service = BetaFlight(setting.port)
        beta_flight_client = BetaFlightClient(beta_flight_service)
        beta_flight_manager = WriteCli(beta_flight_client, beta_flight_config)
        firmware_service = FirmwareService()
        firmware_client = FirmwareClient(firmware_service)
        firmware_manager = FirmwareManager(firmware_client, beta_flight_client, beta_flight_firmware)
        wifi_service = WifiConfig()
        http_service = HttpService(ExpressLRSURL.URL)
        wifi_client = WifiConfigClient(wifi_service, http_service)
        wifi_manager = WifiSearch(wifi_client,
                                  setting.current_wifi,
                                  setting.current_wifi_password,
                                  rx_config)
        if beta_flight_firmware:
            response.beta_flight_firmware = ConfigResponse(**firmware_manager.run())
        if beta_flight_config:
            response.beta_flight_config = ConfigResponse(**beta_flight_manager.run())
        if rx_config:
            response.rx_config = ConfigResponse(**wifi_manager.run())
        return response
