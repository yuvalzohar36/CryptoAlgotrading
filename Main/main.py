import json
import time

import Coins.CoinsManager as CManager
import TradeWallets.WalletManager as WManager
from TradeWallets.BinanceWallet import BinanceWallet
import telegramBot
from threading import Thread
from CryptoUtil.DataUtil import DataUtil

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
        t1 = Thread(target=telegramBot.main_tg_bot, args=(binance_wallet, telegram_bot_token, delay,))
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

    # binance_wallet.invest_on_currency("USDT", 1)
    binance_wallet.invest_on_currency("BTC",0.5)
    binance_wallet.invest_on_currency("LUNC", 0.5)
    binance_wallet.invest_on_currency("DOGE", 0.5)
    binance_wallet.invest_on_currency("LTC", 0.5)
    binance_wallet.invest_on_currency("SHIB", 0.5)

    #binance_wallet.convert("LUNC", "USDT", 0.5)

    # DU = DataUtil(config, local_config, "TEST")  # TEST / LIVE
    # CM = CManager.CoinsManager(DU)
    # WM = WManager.WalletManager([binance_wallet], CM, DU)

    # binance_wallet2.convert("LTC", "DOGE", 0.01)
    #
    # init_indicators_manager(TRADE_ON)

    # CM = CManager.CoinsManager(config, local_config)
    # binance_wallet = BinanceWallet(api_key, api_secret, 0.1, USERNAME, config)
    # WM = WManager.WalletManager([binance_wallet], CM)

<<<<<<< HEAD
    #binance_wallet2 = BinanceWallet(api_key, api_secret, 0.1, USERNAME2, config)
    #execute_telegram_bot(True, binance_wallet2, config)
    while True:
        pass

        time.sleep(5)
  #  binance_wallet2.convert("LTC", "DOGE", 0.01)
=======
    # binance_wallet2 = BinanceWallet(api_key, api_secret, 0.1, USERNAME2, config)
    # execute_telegram_bot(True, binance_wallet2, config)
   # while True:
    #    time.sleep(10)
>>>>>>> cc84df888e2845932c86b99598de7bcd81422db0
