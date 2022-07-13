import time
from threading import Thread
import pandas_datareader as web
from Indicators.Indicator import Indicator
import datetime as dt


class EMAIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, semaphore):
        super().__init__(coin_manager, logger, assessment_df, semaphore)
        self.connection = Indicator.connect(self.api_key, self.api_secret)

    def check(self, args):
        self.result.set_result("BUY")
        self.write_result_to_DB(type(self).__name__)

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
