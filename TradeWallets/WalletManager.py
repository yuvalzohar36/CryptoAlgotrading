import time


class WalletManager:
    def __init__(self, wallets, coin_manager):
        self.wallets = wallets
        self.coin_manager = coin_manager
        while True:
            self.coin_manager.schedule_all_indicators_jobs()
            time.sleep(900)
            print("BTC", self.coin_manager.stats("BTC").assessment())
            print("LTC", self.coin_manager.stats("LTC").assessment())
            print("BURGER", self.coin_manager.stats("BURGER").assessment())
            print("INVERSTING")
            self.invest()

    def add_wallet(self, wallet):
        self.wallets.append(wallet)

    def invest(self):
        for coin in self.coin_manager.coins.keys():
            result = self.coin_manager.stats(coin).assessment()
            if result == "BUY":
                self.wallets[0].invest_on_currency(coin, 0.5)

            elif result == "SELL":
                abort_coin = self.coin_manager.config["ABORT_COIN"]
                self.wallets[0].convert(self, coin, abort_coin, 0.5)
