import time

class WalletManager:
    def __init__(self, wallets, coin_manager):
        self.wallets = wallets
        self.coin_manager = coin_manager
        while True:
            print(self.coin_manager.result_per_coin("BTC").symbol, self.coin_manager.result_per_coin("BTC").result,
                  self.coin_manager.result_per_coin("BTC").credit_average,
                  self.coin_manager.result_per_coin("BTC").indicators_amount)
            print(self.coin_manager.result_per_coin("LTC").symbol, self.coin_manager.result_per_coin("BTC").result,
                  self.coin_manager.result_per_coin("LTC").credit_average,
                  self.coin_manager.result_per_coin("LTC").indicators_amount)
            print(self.coin_manager.result_per_coin("BURGER").symbol, self.coin_manager.result_per_coin("BTC").result,
                  self.coin_manager.result_per_coin("BURGER").credit_average,
                  self.coin_manager.result_per_coin("BURGER").indicators_amount)
            time.sleep(16)

    def add_wallet(self, wallet):
        self.wallets.append(wallet)
