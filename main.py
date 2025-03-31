from typing import Optional

from src.client.betaflight import BetaFlightClient
from src.const import ExpressLRSURL
from src.managers import WriteCli, WifiSearch
import argparse

from src.service import BetaFlight, WifiConfig
from src.service.http_service import HttpService

parser = argparse.ArgumentParser('Apply the betaflight configs')
parser.add_argument('--usb_port', type=str, help='What usb_port to read', default=None)
parser.add_argument('--beta_flight_config', type=str, help='Path to config file', default=None)
parser.add_argument('--rx_config', type=str, help='Path to config file for the RX', default=None)
parser.add_argument('--current_wifi',
                    type=str,
                    help='Name of the wifi you want to reconnect to when the RX config will be applied',
                    default=None)
parser.add_argument('--current_wifi_password',
                    type=str,
                    help='Password of the wifi you want to reconnect to when the RX config will be applied',
                    default=None)


arguments = parser.parse_args()


if __name__ == '__main__':
    if arguments.beta_flight_config:
        service = BetaFlight(arguments.port)
        client = BetaFlightClient(service)
        manager = WriteCli(client, arguments.beta_flight_config)
        manager.run()
    if arguments.rx_config:
        wifi_service = WifiConfig()
        http_service = HttpService(ExpressLRSURL.URL)
        wifi_manager = WifiSearch(wifi_service,
                                  http_service,
                                  arguments.current_wifi,
                                  arguments.current_wifi_password,
                                  arguments.rx_config)
        wifi_manager.run()

