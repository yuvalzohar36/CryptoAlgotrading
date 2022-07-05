import json
from Indicators.IndicatorManager import IndicatorManager
from TradeWallets.BinanceWallet import BinanceWallet
import telegramBot
from threading import Thread

LOCAL_CONFIGURATION_FILE = "local_configuration.json"
CONFIGURATION_FILE = "configuration.json"

TELEGRAM_BOT = False
TRADE_ON = True

if __name__ == '__main__':
    with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
        local_config = json.load(local_config_file)
    with open(CONFIGURATION_FILE) as config_file:
        config = json.load(config_file)

    api_key = local_config["Details"]["api_key"]
    api_secret = local_config["Details"]["api_secret"]

    binance_wallet = BinanceWallet(api_key, api_secret, 0.1, "yuvalbadihi", config)

    binance_wallet.convert("LTC", "DOGE", 0.01)

    join_lst = []

    # if TELEGRAM_BOT:
    #     telegram_bot_token = local_config["Details"]["telegram_bot_token"]
    #     t1 = Thread(target=telegramBot.main_tg_bot, args=(binance_wallet, telegram_bot_token,))
    #     t1.start()
    #     join_lst.append(t1)

    if TRADE_ON:
        indicator_manager = IndicatorManager()


