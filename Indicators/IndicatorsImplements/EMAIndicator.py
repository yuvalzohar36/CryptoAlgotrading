import random
import time

import pandas_datareader as web
from Indicators.Indicator import Indicator
import datetime as dt


class EMAIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, semaphore):
        super().__init__(coin_manager, logger, assessment_df, semaphore)
        self.connection = Indicator.connect(self.api_key, self.api_secret)
        self.days_measure = 10


    def check(self, args):
        while (True):
            time.sleep(4)
         #   data = self.prepare_data(self.days_measure)
        #    ma = self.calculate_ma(data['Close'])
           # data = self.prepare_data(2)
          #  time.sleep(3)
            x = random.randint(1,100)
            if x < 40:
                self.result.set_result('SELL')
            elif x < 60:
                self.result.set_result('HOLD')
            else:
                self.result.set_result('BUY')


    @staticmethod
    def calculate_ma(data):
        sum = 0
        for tup in data:
            sum += int(tup)
        return sum / len(data)

    def prepare_data(self, days_measure):
        time.sleep(1)
        crypto_currency = self.args[0].symbol
        against_currency = 'USD'
        end = dt.datetime.now()
        d = dt.timedelta(days=days_measure - 1)
        start = end - d
        data = 9#web.DataReader(f'{crypto_currency}-{against_currency}', 'yahoo', start, end)
        return data
