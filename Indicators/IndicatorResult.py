class IndicatorResult:
    def __init__(self, indicator, coin):
        self.coin = coin
        self.indicator = indicator
        self.result_setted = False
        self.percent_result = None  # 0--> INFINITY

    def set_result_setted(self):
        self.result_setted = True

    def set_percent_result(self, percent):
        self.percent_result = percent
