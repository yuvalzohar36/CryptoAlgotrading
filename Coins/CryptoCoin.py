from Coins import CoinMarketCap as CMC


class CryptoCoin:
    def __init__(self, symbol, local_config, config):
        self.config = config
        self.local_config = local_config
        self.symbol = symbol
        self.max_attributes_val = self.config["IndicatorsData"]["indicators_attributes_data"]["max_attributes_val"]

        #  attributes
        self.stability = 0
        self.security = 0
        self.scalability = 0
        self.supply = self.get_supply()
        self.decentralisation = 0
        self.demand = 0
        self.usefulness = 0
        self.backup_date = 0

        # Indicators results (DO NOT DELETE)
        self.indicators_results = []

    def exec_indicator(self, indicator):
        self.indicators_results.append(indicator.execute())

    def init_indicators_results(self):
        self.indicators_results = []

    def get_data(self):
        try:
            data = CMC.CoinMarketCap.get_data(self.symbol, self.local_config)
            return data['data'][self.symbol]
        except Exception as e1:
            print(e1, " (Should be added to a log!)")

    def get_name(self):
        return self.get_data()['name']

    def get_supply(self):
        try:
            get_supply_capacity_effect = 1
            return self.get_supply_capacity()*get_supply_capacity_effect

        except Exception as e1:
            print(e1, " (Should be added to a log!)")
            return 0

    def get_max_attributes_val(self):
        return self.max_attributes_val

    def get_supply_capacity(self):
        try:
            return self.get_data()["circulating_supply"] // self.get_data()["max_supply"]

        except Exception as e1:
            print(e1, " (Should be added to a log!)")
            return 0

