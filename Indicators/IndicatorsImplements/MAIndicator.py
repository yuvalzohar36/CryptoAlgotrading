import random
import time
from threading import Thread
import pandas_datareader as web
from Indicators.Indicator import Indicator
import datetime as dt


class MAIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, semaphore):
        super().__init__(coin_manager, logger, assessment_df, semaphore)
        self.connection = Indicator.connect(self.api_key, self.api_secret)
        self.days_measure = 10

    def check(self, args):
        while(True):
            time.sleep(8)
            data = self.prepare_data(self.days_measure)
            ma = self.calculate_ma(data['Close'])
            data = self.prepare_data(2)
            x = random.randint(1, 100)
            time.sleep(3)
            if ma / data['Close'][0] > 1:

                self.result.set_result(x)
            elif ma / data['Close'][0] == 1:
                self.result.set_result(x)
            else:
                self.result.set_result(x)

            #self.write_result_to_DB(type(self).__name__) # GET IT OUT OF HERE

    def improve(self, args):
        self.days_measure = random.randint(7,30)

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
