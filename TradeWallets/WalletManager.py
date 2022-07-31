import time
from datetime import datetime, timedelta



class WalletManager:
    def __init__(self, wallets, coin_manager, data_util):
        self.wallets = wallets
        self.coin_manager = coin_manager
        self.data_util = data_util


        date = datetime(2022, 7, 30, 0, 0)
        while True:
            data_util.set_date(date)
            self.coin_manager.schedule_all_indicators_jobs()
         #   time.sleep(900)
            print("BTC", self.coin_manager.stats("BTC").assessment())
            #print("LTC", self.coin_manager.stats("LTC").assessment())
          #  print("BURGER", self.coin_manager.stats("BURGER").assessment())
            print("INVERSTING")
        #    self.invest()
            print("done!")
            date = date + timedelta(minutes=15)


    def add_wallet(self, wallet):
        self.wallets.append(wallet)

    def invest(self):
        for coin in self.coin_manager.coins.keys():
            result = self.coin_manager.stats(coin).assessment()
            if result == "BUY":
                self.wallets[0].invest_on_currency(coin, 1)

            elif result == "SELL":
                abort_coin = self.coin_manager.config["ABORT_COIN"]
                self.wallets[0].convert(self, coin, abort_coin, 1)
