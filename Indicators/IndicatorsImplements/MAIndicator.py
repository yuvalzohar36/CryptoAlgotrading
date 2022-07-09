import time
from threading import Thread
import pandas_datareader as web
from Indicators.Indicator import Indicator
import datetime as dt

from Indicators import IndicatorResult as IR


class MAIndicator(Indicator):
    def __init__(self, coin_manager):
        super().__init__(coin_manager)
        self.connection = Indicator.connect(self.api_key, self.api_secret)
        self.init_logger(type(self).__name__, self.config)

    def execute(self, args):
        self.result = IR.IndicatorResult(self, args[0])
        self.args = args
        t1 = Thread(target=self.check, args=())
        self.coin_manager.append_new_thread(self, t1)
        t1.start()

    def check(self):
        time.sleep(5)
        days_measure = 14
        data = self.prepare_data(days_measure)
        ma = self.calculate_ma(data['Close'])
        data = self.prepare_data(2)
        self.result.set_percent_result(ma / data['Close'][1])
        self.result.set_result_setted()

    def get_results(self):
        return self.result

    def calculate_ma(self, data):
        sum = 0
        for tup in data:
            sum += int(tup)
        return sum / len(data)

    def prepare_data(self, days_measure):
        crypto_currency = 'BTC'
        against_currency = 'USD'
        end = dt.datetime.now()
        d = dt.timedelta(days=days_measure - 1)
        start = end - d
        data = web.DataReader(f'{crypto_currency}-{against_currency}', 'yahoo', start, end)
        return data
