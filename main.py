import json

import Convertions
from WalletTrading import Wallet
import telegramBot
from threading import Thread

LOCAL_CONFIGURATION_FILE = "configuration.json"
BINANCE_CONVERTIONS = "binanceConvertions.json"

TELEGRAM_BOT = False

if __name__ == '__main__':
    with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
        local_config = json.load(local_config_file)

    api_key = local_config["Details"]["api_key"]
    api_secret = local_config["Details"]["api_secret"]

    convertion = Convertions.Convert(BINANCE_CONVERTIONS)
    wallet = Wallet(api_key, api_secret, convertion, 0.1)
    wallet.invest_on_currency("ETH", 1)
    if (TELEGRAM_BOT):
        telegram_bot_token = local_config["Details"]["telegram_bot_token"]
        t = Thread(target=telegramBot.main_tg_bot, args=(wallet, telegram_bot_token,))
        t.start()

    # wallet.all_in("BTC")

