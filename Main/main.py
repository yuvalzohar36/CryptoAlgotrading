import json
import time

import Coins.CoinsManager as CManager
import TradeWallets.WalletManager as WManager
from TradeWallets.BinanceWallet import BinanceWallet
import telegramBot
from threading import Thread

LOCAL_CONFIGURATION_FILE = "../Configurations/local_configuration.json"
CONFIGURATION_FILE = "../Configurations/configuration.json"

USERNAME = 'yuvalbadihi'
USERNAME2 = 'yuvalzohar'


def execute_telegram_bot(TELEGRAM_BOT, binance_wallet, config):
    if TELEGRAM_BOT:
        join_lst = []
        telegram_bot_token = local_config["TelegramBot"]["telegram_bot_token"]
        delay = config["TradeDetail"]["update_step_size"] * config["TradeDetail"][
            "minutes"] * 60
        t1 = Thread(target=telegramBot.main_tg_bot, args=(binance_wallet, telegram_bot_token,delay,))
        t1.start()
        join_lst.append(t1)


def init_indicators_manager(TRADE_ON):
    if bool(TRADE_ON):
        pass


if __name__ == '__main__':
    with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
        local_config = json.load(local_config_file)
    with open(CONFIGURATION_FILE) as config_file:
        config = json.load(config_file)
    TELEGRAM_BOT = config["Enablers"]["TELEGRAM_BOT"] == 'True'
    TRADE_ON = config["Enablers"]["TRADE_ON"] == 'True'
    api_key = local_config["Binance"][USERNAME]["Details"]["api_key"]
    api_secret = local_config["Binance"][USERNAME]["Details"]["api_secret"]
    binance_wallet = BinanceWallet(api_key, api_secret, 0.1, USERNAME, config)
    execute_telegram_bot(TELEGRAM_BOT, binance_wallet, config)

    CM = CManager.CoinsManager(config, local_config)
    WM = WManager.WalletManager([binance_wallet], CM)

    # binance_wallet2 = BinanceWallet(api_key, api_secret, 0.1, USERNAME2, config)
    # binance_wallet2.convert("LTC", "DOGE", 0.01)
    # binance_wallet2.convert("LTC", "DOGE", 0.01)
    #
    # init_indicators_manager(TRADE_ON)

    # CM = CManager.CoinsManager(config, local_config)
    # binance_wallet = BinanceWallet(api_key, api_secret, 0.1, USERNAME, config)
    # WM = WManager.WalletManager([binance_wallet], CM)

    #binance_wallet2 = BinanceWallet(api_key, api_secret, 0.1, USERNAME2, config)
    #execute_telegram_bot(True, binance_wallet2, config)
    while True:
        pass

        time.sleep(5)
  #  binance_wallet2.convert("LTC", "DOGE", 0.01)
