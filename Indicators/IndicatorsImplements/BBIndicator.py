import pandas_datareader as web
from Indicators.Indicator import Indicator
import datetime as dt
import math


class BBIndicator(Indicator):
    def init(self, coin_manager, logger, assessment_df, semaphore):
        super().init(coin_manager, logger, assessment_df, semaphore)
        self.connection = Indicator.connect(self.api_key, self.api_secret)

    def check(self, args):
        days_measure = 20
        data = self.prepare_data(days_measure)
        ma = self.calculate_ma(data['Close'])
        sd = self.calculate_standard_deviaton(data['Close'], ma)
        data = self.prepare_data(2)
        upper = ma + 2 * sd
        lower = ma - 2 * sd
        curr_value_mean_gap = (data['Close'][1] / ma)
        if curr_value_mean_gap > 1:
            result = (upper / data['Close'][1])
            if result < 1:
                self.result.set_result(888888)  # above upper band
            else:
                self.result.set_result(1 +7878)  # above mean, below upper
        else:
            result = data['Close'][1] / lower
            if result < 1:
                self.result.set_percent_result(1.99)  # below lower band
            else:
                self.result.set_result(18888)  # below mean, above lower
        self.write_result_to_DB(type(self).__name__)


    @staticmethod
    def calculate_ma(data):
        sum = 0
        for tup in data:
            sum += int(tup)
        return sum / len(data)

    @staticmethod
    def calculate_standard_deviaton(data, mean):
        sum = 0
        for tup in data:
            sum += (int(tup) - mean)*(int(tup) - mean)
        to_root = sum / len(data)
        sd = math.sqrt(to_root)
        return sd

    def prepare_data(self, days_measure):
        crypto_currency = self.args[0].symbol
        against_currency = 'USD'
        end = dt.datetime.now()
        d = dt.timedelta(days=days_measure - 1)
        start = end - d
        data = web.DataReader(f'{crypto_currency}-{against_currency}', 'yahoo', start, end)
        return data