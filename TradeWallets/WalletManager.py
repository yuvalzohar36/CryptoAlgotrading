import time
from Tests.indiTest import indiTest
from Coins.CryptoCoin import CryptoCoin
from Indicators.IndicatorsImplements.MAIndicator import MAIndicator as MA


class WalletManager:
    def __init__(self, wallet, coin_manager):
        self.wallets = wallet
        self.coin_manager = coin_manager
        self.MAIndicator = MA(self.coin_manager)
        self.activate_indicator(self.MAIndicator, "BTC")
        # print("YUVAL")
        # self.join_thread(self.MAIndicator)
        while True:
            print("BTC: ", self.get_indicator_result(self.MAIndicator))
            time.sleep(1)

    def add_wallet(self, wallet):
        self.wallets.append(wallet)

    def join_thread(self, indicator):
        self.coin_manager.current_indicators_threads[indicator].join()

    def activate_indicator(self, indicator, symbol):
        self.coin_manager.indicator_activate(indicator, [symbol])

    def get_indicator_result(self, indicator):
        res_obj = self.coin_manager.recv_indicator_result(indicator)
        if res_obj.result_setted:
            return self.coin_manager.recv_indicator_result(indicator).percent_result
        return -1  # no result yet
