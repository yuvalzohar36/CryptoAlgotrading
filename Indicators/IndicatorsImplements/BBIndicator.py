import pandas_datareader as web
from Indicators.Indicator import Indicator
import datetime as dt
import math


class BBIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, semaphore):
        super().__init__(coin_manager, logger, assessment_df, semaphore)
        self.candles_measure = 20
        self.steps = super().get_config()["TradeDetail"]["update_step_size"]
        self.mins = super().get_config()["TradeDetail"]["minutes"]
        self.coin = None

    def run(self, args):
        self.coin = args[0]
        data = self.prepare_data()
        ma = self.calculate_ma(data)
        sd = self.calculate_standard_deviaton(data, ma)
        upper = ma + 2 * sd
        lower = ma - 2 * sd
        self.res(lower, ma, upper)


    @staticmethod
    def calculate_ma(data):
        sum = 0
        for tup in data:
            sum += float(tup)
        return sum / len(data)

    @staticmethod
    def calculate_standard_deviaton(data, mean):
        sum = 0
        for tup in data:
            sum += (float(tup) - mean)*(float(tup) - mean)
        to_root = sum / len(data)
        sd = math.sqrt(to_root)
        return sd

    def prepare_data(self):
        interval = 0
        close_set = []
        for kline in super().get_binance_module().client.get_historical_klines_generator(f"{self.coin.symbol}USDT",
                                                                                         super().get_binance_module().client.KLINE_INTERVAL_15MINUTE,
                                                                                         f"{self.steps * self.mins * self.candles_measure} minutes ago UTC"):
            if interval % self.steps == 0:
                close_set.append(kline[1])
            interval += 1
        return close_set

    def res(self, lower, ma, upper):
        curr_price = super().get_binance_module().currency_price(self.coin.symbol)
        if curr_price <= lower:
            self.result.set_result('BUY')
        elif curr_price >= upper:
            self.result.set_result('SELL')
        else:
            self.result.set_result('HOLD')

