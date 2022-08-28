import json
import time
import warnings
from datetime import datetime, timedelta

import Coins.CoinsManager as CManager
import TradeWallets.WalletManager as WManager
from TradeWallets.BinanceWallet import BinanceWallet
import telegramBot
from threading import Thread
from CryptoUtil.DataUtil import DataUtil
from TradeWallets.TestWallet import TestWallet

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
    MODE = "TEST"  # TEST / LIVE

    warnings.filterwarnings("ignore")
    with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
        local_config = json.load(local_config_file)
    with open(CONFIGURATION_FILE) as config_file:
        config = json.load(config_file)
    TELEGRAM_BOT = config["Enablers"]["TELEGRAM_BOT"] == 'True'
    TRADE_ON = config["Enablers"]["TRADE_ON"] == 'True'
    api_key = local_config["Binance"][USERNAME]["Details"]["api_key"]
    api_secret = local_config["Binance"][USERNAME]["Details"]["api_secret"]

    # execute_telegram_bot(TELEGRAM_BOT, binance_wallet, config)

    if MODE == "TEST":
        threads = []
        date = datetime(2020, 7, 17, 3, 0)
        for i in range(24):
            DU = DataUtil(config, local_config, MODE, date, date + timedelta(days=7))  # TEST / LIVE
            CM = CManager.CoinsManager(DU)
            TW = TestWallet(DU)
            threads.append(Thread(target=WManager.WalletManager, args=([TW], CM, DU)))
            date = date + timedelta(days=30)
        print(threads)
        for i in range(24):
            threads[i].start()



    else:
        DU = DataUtil(config, local_config, MODE)  # TEST / LIVE
        CM = CManager.CoinsManager(DU)
        binance_wallet = BinanceWallet(api_key, api_secret, 0.1, USERNAME, config)
        WM = WManager.WalletManager([binance_wallet], CM, DU)
    for i in range(24):
        threads[i].join()
    print("DONE")
    while True:
        time.sleep(10)
