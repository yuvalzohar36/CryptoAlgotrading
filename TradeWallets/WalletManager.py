import time
from Tests.indiTest import indiTest
from Coins.CryptoCoin import CryptoCoin
from Indicators.IndicatorsImplements.MAIndicator import MAIndicator as MA


class WalletManager:
    def __init__(self, wallets, coin_manager):
        self.wallets = wallets
        self.coin_manager = coin_manager
        while True:
            print(self.coin_manager.result_per_coin("BTC"))
            print(self.coin_manager.result_per_coin("LTC"))
            print(self.coin_manager.result_per_coin("BURGER"))
            time.sleep(16)

    def add_wallet(self, wallet):
        self.wallets.append(wallet)
