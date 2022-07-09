import time
from Tests.indiTest import indiTest
from Coins.CryptoCoin import CryptoCoin
from Indicators.IndicatorsImplements.MAIndicator import MAIndicator as MA


class WalletManager:
    def __init__(self, wallet, coin_manager):
        self.wallets = wallet
        self.coin_manager = coin_manager
        while True:
            print(self.coin_manager.result_per_coin("BTC"))
            print(self.coin_manager.result_per_coin("LTC"))
            time.sleep(3)



    def add_wallet(self, wallet):
        self.wallets.append(wallet)



