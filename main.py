import json

import binance.exceptions
from binance.client import Client
import pprint

import Convertions
from WalletTrading import Wallet

LOCAL_CONFIGURATION_FILE = "configuration.json"
BINANCE_CONVERTIONS = "binanceConvertions.json"

if __name__ == '__main__':
    with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
        local_config = json.load(local_config_file)

    api_key = local_config["Details"]["api_key"]
    api_secret = local_config["Details"]["api_secret"]
    convertion = Convertions.Convert(BINANCE_CONVERTIONS)
    wallet = Wallet(api_key, api_secret,convertion,0.1)
    wallet.all_in("BTC")


