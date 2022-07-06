import time
from threading import Thread
import TradeWallets.BinanceWallet as BW

from Indicators.Indicator import Indicator


class indiTest(Indicator):
    def __init__(self):
        super().__init__()
        self.connection = Indicator.connect(self.api_key, self.api_secret)
        self.results = [0.0, 0.0]
        self.init_logger(type(self).__name__, self.config)

    def execute(self, args):
        self.args = args
        t1 = Thread(target=self.check, args=())
        t1.start()

    def check(self):
        last_update = 0
        while True:
            val = self.get_depth(self.args, "USDT")
            current_update = val['lastUpdateId']
            if last_update != current_update:
                last_update = current_update
                for bid in val['bids']:
                    if float(bid[1]) > 1000000:
                        self.results[0] = float(bid[1])
                        self.logger.info(f"Bought {float(bid[1])}, Currency : {self.args}")

                for ask in val['asks']:
                    if float(ask[1]) > 1000:
                        self.results[1] = float(ask[1])
                        self.logger.info(f"Sold {float(ask[1])}, Currency: {self.args}")
            time.sleep(15)

    def get_results(self):
        return self.results

    def get_depth(self, first_coin, second_coin):
        try:
            symbol = BW.BinanceWallet.get_symbol(first_coin, second_coin)
            depth = self.connection.get_order_book(symbol=symbol)
            return depth
        except Exception as ex:
            self.logger.error(f"Error {ex}")
            return 0
