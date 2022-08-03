import random

from Indicators.Indicator import Indicator


class CWMAIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, data_util):
        super().__init__(coin_manager, logger, assessment_df, data_util)
        self.candles_measure = 30
        self.steps = super().get_config()["TradeDetail"]["update_step_size"]
        self.mins = super().get_config()["TradeDetail"]["minutes"]
        self.coin = None
        self.diff = 0.0018
        self.bad_credit = 0.8

    def run(self, args):
        self.coin = args[0]
        data = self.prepare_data()
        sum = self.get_sum(data)
        self.cal(sum)

    def cal(self, ma):
        self.fix_myself()
        curr_price = super().get_data_util().currency_price(self.coin.symbol)
        if abs(1 - curr_price / ma) < self.diff:
            self.result.set_result('HOLD')
        elif ma > curr_price:
            self.result.set_result('BUY')
        elif curr_price > ma:
            self.result.set_result('SELL')

    def prepare_data(self):
        klines = super().get_data_util().request_historical_data(self.coin.symbol, self.candles_measure)
        lst = []
        for val in klines['Close']:
            lst.append(float(val))
        return lst

    def get_sum(self, data):
        ma = 0
        mult = 1
        pow_sum = 0
        for val in data:
            ma += pow(0.5, mult) * val
            pow_sum += pow(0.5, mult)
            mult += 1
        rest = 1 - pow_sum
        ma += data[0] * rest
        return ma

    def fix_myself(self):
        credit = super().my_credit()
        if credit < self.bad_credit:
            self.candles_measure = random.randint(5, 50)
            super().get_logger().debug(f"New candles_measure {self.candles_measure} for {self.coin.symbol}")





