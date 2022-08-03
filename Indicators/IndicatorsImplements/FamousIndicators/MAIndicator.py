from Indicators.Indicator import Indicator


class MAIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, data_util):
        super().__init__(coin_manager, logger, assessment_df, data_util)
        self.candles_measure = 10
        self.steps = super().get_config()["TradeDetail"]["update_step_size"]
        self.mins = super().get_config()["TradeDetail"]["minutes"]
        self.coin = None
        self.diff = 1.0

    def run(self, args):
        self.coin = args[0]
        data = self.prepare_data()
        sum = self.get_sum(data)
        self.cal(sum)

    def cal(self, sum):
        ma = sum / self.candles_measure

        curr_price = super().get_data_util().currency_price(self.coin.symbol)
        if ma > self.diff * curr_price:
            self.result.set_result('BUY')
        elif curr_price > self.diff * ma:
            self.result.set_result('SELL')
        else:
            self.result.set_result('HOLD')

    def prepare_data(self):
        klines = super().get_data_util().request_historical_data(self.coin.symbol, self.candles_measure)
        lst = []
        for val in klines['Close']:
            lst.append(float(val))

        return lst

    def get_sum(self, data):
        sum = 0
        for val in data:
            sum += val
        return sum