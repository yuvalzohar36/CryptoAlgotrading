import time
from datetime import datetime, timedelta


class WalletManager:
    def __init__(self, wallets, coin_manager, data_util):
        self.wallets = wallets
        self.coin_manager = coin_manager
        self.data_util = data_util
        self.mins = data_util.config["TradeDetail"]["minutes"]  # append 'm'
        self.steps = data_util.config["TradeDetail"]["update_step_size"]

        date = datetime(2022, 7, 17, 3, 0)
        while True:
            data_util.set_date(date)
            self.coin_manager.schedule_all_indicators_jobs()
            if data_util.mode == 'LIVE':
                time.sleep(self.mins * self.steps * 60)

            self.data_util.lock('MW_all_indi_finish_sem')
            print("BTC", self.coin_manager.stats("BTC").assessment())
            print("LTC", self.coin_manager.stats("LTC").assessment())
            # print("BURGER", self.coin_manager.stats("BURGER").assessment())
            self.invest()
            date = date + timedelta(minutes=60)

    def add_wallet(self, wallet):
        self.wallets.append(wallet)

    def invest(self):
        for coin in self.coin_manager.coins.keys():
            result = self.coin_manager.stats(coin).assessment()
            if result == "BUY":
                self.wallets[0].invest_on_currency(coin, 0.5)

            elif result == "SELL":
                abort_coin = self.coin_manager.config["ABORT_COIN"]
                self.wallets[0].convert(coin, abort_coin, 0.5)

    def get_longest_indicator_duration(self):
        max_duration = 0
        for indicator in self.data_util.config["Indicators"]:
            indicator = self.data_util.config["Indicators"][indicator]
            if indicator["MODE"] == 'ON' and indicator['DURATION'] > max_duration:
                max_duration = indicator['DURATION']
        return max_duration
