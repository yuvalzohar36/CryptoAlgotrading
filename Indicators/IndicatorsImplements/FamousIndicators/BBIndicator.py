import time
from Indicators.Indicator import Indicator
import math


class BBIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, data_util):
        super().__init__(coin_manager, logger, assessment_df, data_util)
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
        self.res(lower, upper)

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
            sum += (float(tup) - mean) * (float(tup) - mean)
        to_root = sum / len(data)
        sd = math.sqrt(to_root)
        return sd

    def prepare_data(self):
        data = super().get_data_util().request_historical_data(self.coin.symbol, self.candles_measure)
        lst = []
        for i in data["Close"]:
            lst.append(float(i))
        return lst

    def res(self, lower, upper):
        curr_price = super().get_data_util().currency_price(self.coin.symbol)
        if curr_price <= lower:
            self.result.set_result('BUY')
        elif curr_price >= upper:
            self.result.set_result('SELL')
        else:
            self.result.set_result('HOLD')

