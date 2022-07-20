import time

class WalletManager:
    def __init__(self, wallets, coin_manager):
        self.wallets = wallets
        self.coin_manager = coin_manager
        while True:
            self.coin_manager.stats("BTC")
            self.coin_manager.stats("LTC")
         #   self.coin_manager.stats("BURGER")
           # print(x.assessment())
           # print(x.result_creation)
            time.sleep(20)

    def add_wallet(self, wallet):
        self.wallets.append(wallet)
