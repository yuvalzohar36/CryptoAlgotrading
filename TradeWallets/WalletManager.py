import time
from datetime import datetime, timedelta

import time


class WalletManager:
    def __init__(self, wallets, coin_manager, data_util):
        self.wallets = wallets
        self.coin_manager = coin_manager
        self.data_util = data_util
        self.mins = data_util.config["TradeDetail"]["minutes"]  # append 'm'
        self.steps = data_util.config["TradeDetail"]["update_step_size"]
        self.results_dicts = self.init_symbols()
        while True:
            print(f"Date - {self.data_util.to_date}")

            start_time = time.time()

            self.coin_manager.schedule_all_indicators_jobs()

            if data_util.mode == 'LIVE':
                time.sleep(self.mins * self.steps * 60)

            self.data_util.lock('MW_all_indi_finish_sem')

            for coin in self.results_dicts.keys():
                stat = self.coin_manager.stats(coin)
                self.results_dicts.update({coin: stat})
            self.invest()
            print("--- %s seconds ---" % (time.time() - start_time))
            print()
            self.data_util.to_date = self.data_util.to_date + timedelta(minutes=self.mins * self.steps)
            if data_util.mode == 'TEST' and data_util.end_date <= self.data_util.to_date:
                return

    def add_wallet(self, wallet):
        self.wallets.append(wallet)

    def invest(self):
        for coin in self.coin_manager.coins.keys():
            result = self.results_dicts[coin].assessment()
            print(f"Coin : {coin}, Result: {result}")
            if result == "BUY":
                for wallet in self.wallets:
                    wallet.buy(coin, 0.5)

            elif result == "SELL":
                for wallet in self.wallets:
                    wallet.sell(coin, 0.5)
        self.wallets[0].report()

    def get_longest_indicator_duration(self):
        max_duration = 0
        for indicator in self.data_util.config["Indicators"]:
            indicator = self.data_util.config["Indicators"][indicator]
            if indicator["MODE"] == 'ON' and indicator['DURATION'] > max_duration:
                max_duration = indicator['DURATION']
        return max_duration

    def init_symbols(self):
        results_dict = {}
        for coin in self.coin_manager.coins.keys():
            results_dict[coin] = None
        return results_dict
