from Indicators.Indicator import Indicator
import talib as tb
import numpy


class RSIIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, semaphore, data_util):
        super().__init__(coin_manager, logger, assessment_df, semaphore, data_util)
        self.timeperiod = 8
        self.RSI_OVERBOUGHT = 70
        self.RSI_OVERSOLD = 30
        self.overbought_diff = 1
        self.oversold_diff = 1
        self.multi = 2

    def run(self, args):
        self.coin = args[0]
        rsi = self.get_rsi(self.prepare_data())
        self.res(rsi[-1])

    def get_rsi(self, close):
        real = tb.RSI(close, timeperiod=self.timeperiod)
        return real

    def prepare_data(self):
        data = super().get_data_util().request_historical_data(self.coin.symbol, self.timeperiod * self.multi)
        lst = []
        for i in data["Close"]:
            lst.append(float(i))
        lst.reverse()
        return numpy.array(lst)

    def res(self, rsi):
        if self.RSI_OVERBOUGHT * self.overbought_diff <= rsi:
            self.result.set_result('SELL')
        elif self.RSI_OVERSOLD * self.oversold_diff >= rsi:
            self.result.set_result('BUY')
        else:
            self.result.set_result('HOLD')