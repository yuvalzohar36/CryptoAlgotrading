import random
import time
from Indicators.Indicator import Indicator


class MAIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, semaphore):
        super().__init__(coin_manager, logger, assessment_df, semaphore)
        self.candles_measure = 25
        self.diff = 1.0
        self.bad_credit = 0.9
        self.steps = super().get_config()["TradeDetail"]["update_step_size"]
        self.mins = super().get_config()["TradeDetail"]["minutes"]
        self.coin = None

    def run(self, args):
        self.self_consciousness()
        self.coin = args[0]
        interval = 0
        sum = 0
        for kline in super().get_binance_module().client.get_historical_klines_generator(f"{self.coin.symbol}USDT",
                                                                                         super().get_binance_module().client.KLINE_INTERVAL_15MINUTE,
                                                                                         f"{self.steps * self.mins * self.candles_measure} minutes ago UTC"):
            if interval % self.steps == 0:
                sum += float(kline[1])
            interval += 1
        self.cal(sum)
        print("DONEMA")
        # super().sem_credit_updated().acquire()  # wait to get my new credit after giving those values

    def cal(self, sum):
        should_be_price_ma = sum / self.candles_measure
        curr_price = super().get_binance_module().currency_price(self.coin.symbol)
        if should_be_price_ma > self.diff * curr_price:
            self.result.set_result('BUY')
        elif curr_price > self.diff * should_be_price_ma:
            self.result.set_result('SELL')
        else:
            self.result.set_result('HOLD')

    def self_consciousness(self):
        my_new_credit = super().my_credit()
        if my_new_credit < self.bad_credit:
            self.improve()

    def improve(self):
        self.candles_measure = random.randint(7, 30)
        self.diff = random.randint(100, 150) / 100
