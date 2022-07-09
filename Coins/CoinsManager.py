from threading import Thread

from Coins import CryptoCoin as CC


class CoinsManager:
    def __init__(self, config):
        self.config = config
        self.coins = self.init_coins()
        self.current_indicators_threads = {}

    def indicator_activate(self, indicator, args):
        # scan a json file that says which indicators to activate and turn them on.
        args[0] = self.coins[args[0]]  # replace the coin name with its object CryptoCoin
        indicator.execute(args)

    def recv_indicator_result(self, indicator):
        return indicator.get_results()

    def init_coins(self):
        coins = {}
        for coin in self.config["Coins"]:
            if self.config["Coins"][coin] == "ON":
                coins[coin] = CC.CryptoCoin(coin)
        return coins

    def append_new_thread(self, indicator, thread):
        self.current_indicators_threads[indicator] = thread
