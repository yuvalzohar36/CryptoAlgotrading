
class CryptoCoin:
    def __init__(self, symbol):
        self.symbol = symbol
        self.next_hour_price = 0
        self.next_day_price = 0
        self.stability = 0
        self.security = 0
        self.scalability = 0
        self.supply = 0
        self.decentralisation = 0
        self.demand = 0
        self.usefulness = 0
        self.backup_date = 0
        self.indicators_results = []

    def exec_indicator(self, indicator):
        self.indicators_results.append(indicator.execute())

    def init_indicators_results(self):
        self.indicators_results = []