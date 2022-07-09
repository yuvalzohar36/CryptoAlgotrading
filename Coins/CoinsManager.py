from threading import Thread

from Coins import CryptoCoin as CC
from Indicators.IndicatorsImplements.MAIndicator import MAIndicator as MA
import importlib


class CoinsManager:
    def __init__(self, config):
        self.config = config
        self.coins, self.coins_indicators = self.init_coins()
        self.current_indicators_threads = {}
        self.activate_all_indicators()

    @staticmethod
    def indicator_activate(indicator, coin_instance):
        args = [coin_instance]
        indicator.execute(args)

    def activate_all_indicators(self):
        MAIN_PATH = self.config["Paths"]["MAIN_INDICATORS_PATH"]
        for coin in self.coins.keys():
            for indicator in self.config["Indicators"].keys():
                indicator_dict = self.config["Indicators"][indicator]
                module = importlib.import_module(MAIN_PATH + indicator_dict["MODULE_PATH"])
                class_ = getattr(module, indicator_dict["MODULE_PATH"])
                current_indicator = class_(self)
                self.indicator_activate(current_indicator, self.coins[coin])
                self.coins_indicators[coin].append(current_indicator)

    def init_coins(self):
        coins = {}
        coins_indicators = {}
        for coin in self.config["Coins"]:
            if self.config["Coins"][coin]["Mode"] == "ON":
                coins_indicators[coin] = []
                coins[coin] = CC.CryptoCoin(coin)
        return coins, coins_indicators

    def append_new_thread(self, indicator, thread):
        self.current_indicators_threads[indicator] = thread

    def recv_indicator_results(self, symbol):
        results = []
        for indi in self.coins_indicators[symbol]:
            results.append(indi.get_results())
        return results

    def join_thread(self, indicator):
        self.current_indicators_threads[indicator].join()

    def result_per_coin(self, symbol):
        percent = 0
        for result in self.recv_indicator_results(symbol):
            if result.result_setted:
                percent += result.percent_result
        return percent
