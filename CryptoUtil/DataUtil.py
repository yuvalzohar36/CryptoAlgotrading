import json
from datetime import datetime, timedelta

from Indicators.Indicator import Indicator as IndicatorUtil

USERNAME = 'yuvalbadihi'
LOCAL_CONFIGURATION_FILE = "../Configurations/local_configuration.json"
CONFIGURATION_FILE = "../Configurations/configuration.json"


# klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")
# klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

class DataUtil:
    def __init__(self, config, local_config, mode):
        self.config = config
        self.local_config = local_config
        self.mode = mode  # TEST, LIVE
        self.mins = self.config["TradeDetail"]["minutes"]  # append 'm'
        self.steps = self.config["TradeDetail"]["update_step_size"]
        self.client = IndicatorUtil.connect(self.local_config["Binance"][USERNAME]["Details"]["api_key"],
                                            self.local_config["Binance"][USERNAME]["Details"]["api_secret"])
        self.to_date = None

    def request_historical_data(self, symbol, candles_count):
        convert_symbol = symbol + "USDT"
        start_time = f"{self.steps * self.mins * candles_count + 60} minutes ago UTC"
        if self.mode == "LIVE":
            data = self.client.get_historical_klines(symbol + "USDT", str(self.mins) + 'm', start_time)
        else:
            from_date = self.to_date - timedelta(minutes=self.steps * self.mins * candles_count) - timedelta(days=1)
            data = self.client.get_historical_klines(symbol + "USDT", str(self.mins) + 'm',
                                                     from_date.strftime("%d %b, %Y"),
                                                     self.to_date.strftime("%d %b, %Y"))
        print(data)

    def set_date(self, date):
        self.to_date = date


if __name__ == '__main__':
    with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
        local_config = json.load(local_config_file)
    with open(CONFIGURATION_FILE) as config_file:
        config = json.load(config_file)
    s = DataUtil(config, local_config, "TEST")
    s.set_date(datetime(2020, 5, 17))
    s.request_historical_data('BTC', 25)
