from Indicators.Indicator import Indicator


class RSIIndicator(Indicator):
    def init(self, coin_manager, logger, assessment_df, data_util):
        super()._init_(coin_manager, logger, assessment_df, data_util)
        self.candles_measure = 14
        self.steps = super().get_config()["TradeDetail"]["update_step_size"]
        self.mins = super().get_config()["TradeDetail"]["minutes"]
        self.coin = None
        self.diff = 1.0

    def run(self, args):
        self.coin = args[0]
        self.calculate()

    def prepare_data(self):
        klines = super().get_data_util().request_historical_data(self.coin.symbol, self.candles_measure)
        lst = []
        for val in klines['Close']:
            lst.append(float(val))
        return lst[::-1]

    def calculate(self):
        lst = self.prepare_data()
        gainsSum = 0
        lossSum = 0
        last = lst[0]
        RS = 0
        RSI = 0
        now = 0
        result = 0
        for i in range(1, self.candles_measure):

            now = lst[i]
            result = now - last
            if (result) >= 0:
                gainsSum += result
            else:
                lossSum += abs(result)
            last = now

        avgGain = gainsSum / self.candles_measure
        avgLoss = lossSum / self.candles_measure

        if (avgLoss == 0):
            return self.result.set_result('BUY')  # avoid diving by 0, it means price went up all days.

        RS = avgGain / avgLoss
        # print("\nRS IS:",RS)

        RSI = 100 - (100 / (1 + RS))
        if RSI > 70:
            self.result.set_result('SELL')
        elif RSI < 30:
            self.result.set_result('BUY')
        else:
            self.result.set_result('HOLD')

    # rsi: if day closes on positive change, add diff to gain,0 to loss.
    #:after calculations for 14 periods, divide by 14
    # calculate RS: #RS=(AVG Gain)/(AVG Loss)
    # calculate RSI: #rsi=100-(100/1+RS)
    # if rsi above 70 return buy, less than 30 return sell. else return hold.