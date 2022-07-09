import time
from threading import Thread
import pandas_datareader as web
from Indicators.Indicator import Indicator
import datetime as dt


class MAIndicator(Indicator):
    def __init__(self, coin_manager):
        super().__init__(coin_manager)
        self.connection = Indicator.connect(self.api_key, self.api_secret)
        self.init_logger(type(self).__name__, self.config)

    def check(self, args):
        self.logger.info(f"Execute for Symbol {self.args[0].symbol}")
        days_measure = 14
        data = self.prepare_data(days_measure)
        ma = self.calculate_ma(data['Close'])
        data = self.prepare_data(2)
        self.result.set_percent_result(ma / data['Close'][1])
        self.result.set_result_setted()
        self.logger.info(f"Current result for symbol {self.args[0].symbol} is: ")
        self.logger.info(
            f"Percent result is: {self.result.percent_result}")

    @staticmethod
    def calculate_ma(data):
        sum = 0
        for tup in data:
            sum += int(tup)
        return sum / len(data)

    def prepare_data(self, days_measure):
        crypto_currency = self.args[0].symbol
        against_currency = 'USD'
        end = dt.datetime.now()
        d = dt.timedelta(days=days_measure - 1)
        start = end - d
        data = web.DataReader(f'{crypto_currency}-{against_currency}', 'yahoo', start, end)
        return data
