import json
from binance.client import Client
import pprint
from WalletTrading import Wallet

LOCAL_CONFIGURATION_FILE = "configuration.json"


if __name__ == '__main__':
    with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
        local_config = json.load(local_config_file)
    api_key = local_config["Details"]["api_key"]
    api_secret = local_config["Details"]["api_secret"]
    wallet = Wallet(api_key, api_secret)

    print(wallet.get_products())
    #wallet.sell("BTC", "USDT", "MARKET", 0.001)


