from Coins import CoinMarketCap as CMC
import pandas as pd


class CryptoCoin:
    def __init__(self, symbol, local_config, config, coins_df):
        self.config = config
        self.local_config = local_config
        self.symbol = symbol
        self.max_attributes_val = self.config["IndicatorsData"]["indicators_attributes_data"]["max_attributes_val"]
        self.coin_df = coins_df
        #  attributes
        self.stability = 0
        self.security = 0
        self.scalability = 0
        self.supply = 8 #self.get_supply()
        self.decentralisation = 0
        self.demand = 0
        self.usefulness = 0
        self.backup_date = 0
        self.update_coin_data(coins_df)
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
            return self.get_supply_capacity() * get_supply_capacity_effect

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

    def update_coin_data(self, coins_df):
        index = coins_df.index[coins_df['Coin'] == self.symbol]
        coins_df.loc[index.values[0], 'MaxAttributeVal'] = self.max_attributes_val
        coins_df.loc[index.values[0], 'Supply'] = self.get_supply()

    def attributes_refresh(self):
        print(self.get_supply())

    def get_stability(self):
        try:
            # 1h 24h 7d 30d 60d 90d
            sum = 0
            percent_change_x_effect = [0.35, 0.25, 0.20, 0.1, 0.07, 0.03]
            percent_change_x = [self.get_data()["quote"]["USD"]["percent_change_1h"],
                                self.get_data()["quote"]["USD"]["percent_change_24h"],
                                self.get_data()["quote"]["USD"]["percent_change_7d"],
                                self.get_data()["quote"]["USD"]["percent_change_30d"],
                                self.get_data()["quote"]["USD"]["percent_change_60d"],
                                self.get_data()["quote"]["USD"]["percent_change_90d"]]

            for i in range(len(percent_change_x_effect)):
                sum += percent_change_x_effect[i] * percent_change_x[i]

            return sum

        except Exception as e1:
            print(e1, " (Should be added to a log!)")
            return 0
