import random
import time

from Indicators.Indicator import Indicator
import datetime as dt
import math


class RANDMAIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, semaphore):
        super().__init__(coin_manager, logger, assessment_df, semaphore)
        self.candles_measure = random.randint(7, 30)
        self.steps = super().get_config()["TradeDetail"]["update_step_size"]
        self.mins = super().get_config()["TradeDetail"]["minutes"]
        self.coin = None
        self.smoothing = 2
        self.bad_credit = 0.9
        self.diff = random.randint(100, 150) / 100

    def run(self, args):
        while True:
            self.coin = args[0]
            data = self.prepare_data()
            bma = float(self.calculate_bma(data, self.candles_measure, self.smoothing)[0])
            self.cal(bma)
            time.sleep(10)
          #  self.self_consciousness()
         #   time.sleep(self.steps * self.mins - 150)  # IMPROVE!!!

    def calculate_bma(self, prices, days, smoothing=2):
        ema = [sum(prices[:days]) / days]
        for price in prices[days:]:
            ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
        return ema

    def prepare_data(self):
        interval = 0
        close_set = []
        for kline in super().get_binance_module().client.get_historical_klines_generator(f"{self.coin.symbol}USDT",
                                                                                         super().get_binance_module().client.KLINE_INTERVAL_15MINUTE,
                                                                                         f"{self.steps * self.mins * self.candles_measure} minutes ago UTC"):
            if interval % self.steps == 0:
                close_set.append(float(kline[1]))
            interval += 1
        return close_set

    def cal(self, bma):
        curr_price = super().get_binance_module().currency_price(self.coin.symbol)
        if bma > self.diff * curr_price:
            self.result.set_result('BUY')
        elif curr_price > self.diff * bma:
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
