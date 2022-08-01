from Indicators.Indicator import Indicator
import talib as tb
import numpy


class EMAIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, semaphore, data_util):
        super().__init__(coin_manager, logger, assessment_df, semaphore, data_util)
        self.timeperiod = 10
        self.diff = 1

    def run(self, args):
        self.coin = args[0]
        ema = self.get_ema(self.prepare_data())
        self.res(ema[-1])

    def get_ema(self, close):
        real = tb.EMA(close, timeperiod=self.timeperiod)
        return real

    def prepare_data(self):
        data = super().get_data_util().request_historical_data(self.coin.symbol, self.timeperiod + 5)
        lst = []
        for i in data["Close"]:
            lst.append(float(i))
        lst.reverse()
        return numpy.array(lst)

    def res(self, ema):
        curr_price = super().get_data_util().currency_price(self.coin.symbol)
        if ema > self.diff * curr_price:
            self.result.set_result('BUY')
        elif curr_price > self.diff * ema:
            self.result.set_result('SELL')
        else:
            self.result.set_result('HOLD')
