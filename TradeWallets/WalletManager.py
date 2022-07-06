import time
from Tests.indiTest import indiTest


class WalletManager:
    def __init__(self, wallet, coin_manager):
        self.wallets = wallet
        self.coin_manager = coin_manager

        # self.indiTestIndi = indiTest()
        # self.indiTestIndi2 = indiTest()
        # self.coin_manager.indicator_activate(self.indiTestIndi, "BURGER")
        # self.coin_manager.indicator_activate(self.indiTestIndi2, "BTC")
        # self.coin_manager.append_indicator(self.indiTestIndi)

        # time.sleep(4)
        # while(True):
        #     print("BURGER: ", self.coin_manager.recv_indicator_result(self.indiTestIndi))
        #     print("BTC: " ,self.coin_manager.recv_indicator_result(self.indiTestIndi2))
        #
        #     time.sleep(1)

    def add_wallet(self, wallet):
        self.wallets.append(wallet)
