import time

class WalletManager:
    def __init__(self, wallets, coin_manager):
        self.wallets = wallets
        self.coin_manager = coin_manager
        while True:
            print("BTC", self.coin_manager.stats("BTC").assessment())
            print("LTC", self.coin_manager.stats("LTC").assessment())
            print("BURGER", self.coin_manager.stats("BURGER").assessment())
           # print(x.assessment())
           # print(x.result_creation)
            time.sleep(20)

    def add_wallet(self, wallet):
        self.wallets.append(wallet)
