from Coins import CoinMarketCap as CMC
import pandas as pd
import Firebase
from Firebase import FireBaseUtil


class CryptoCoin:
    def __init__(self, symbol, local_config, config, data_util):
        self.config = config
        self.local_config = local_config
        self.symbol = symbol
        self.max_attributes_val = self.config["IndicatorsData"]["indicators_attributes_data"]["max_attributes_val"]
        self.data_util = data_util

        #  attributes
        self.stability = 0
        self.security = 0
        self.scalability = 0
        self.supply = 8
        self.decentralisation = 0
        self.demand = self.get_demand()
        self.usefulness = 0
        self.backup_date = self.get_backup_date()

        # Indicators results (DO NOT DELETE)
        self.indicators_results = []

    def exec_indicator(self, indicator):
        self.indicators_results.append(indicator.execute())

    def init_indicators_results(self):
        self.indicators_results = []

    def attributes_refresh(self, coins_df):
        self.demand = self.get_demand()
        return self.update_coin_data(coins_df)  # Write to pandas

    def update_coin_data(self, coins_df):
        index = coins_df.index[coins_df['Coin'] == self.symbol]
        coins_df.loc[index.values[0], 'Backup_Date'] = self.backup_date
        coins_df.loc[index.values[0], 'MaxAttributeVal'] = self.max_attributes_val
        coins_df.loc[index.values[0], 'Demand'] = self.demand
        return coins_df

    def get_max_attributes_val(self):
        return self.max_attributes_val

    def get_demand(self):
        return self.data_util.get_data(self.symbol, "Volume")

    def get_backup_date(self):
        return self.data_util.get_datetime()


