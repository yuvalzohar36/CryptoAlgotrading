import json
from datetime import datetime, timedelta
import pandas as pd
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
        temp_date = self.to_date + timedelta(days=1)
        start_time = f"{self.steps * self.mins * candles_count + 60} minutes ago UTC"
        if self.mode == "LIVE":
            data = self.client.get_historical_klines(convert_symbol, str(self.mins) + 'm', start_time)
        else:
            from_date = self.to_date - timedelta(minutes=self.steps * self.mins * candles_count) - timedelta(days=2)
            data = self.client.get_historical_klines(convert_symbol, str(self.mins) + 'm',
                                                     from_date.strftime("%d %b, %Y"),
                                                     temp_date.strftime("%d %b, %Y"))

        new_data = []
        for i in data:
            new_data.append(i)
            if str(int(datetime.timestamp(self.to_date))) in str(i[0]):
                break
        bars = new_data


        for line in bars:  # Keep only first 5 columns, "date" "open" "high" "low" "close"
            del line[5:]
        df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])  # 2 dimensional tabular data
        new_df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close'])  # 2 dimensional tabular data

        high, low, close, open, date = 0, float('inf'), 0, 0, 0
        counter = 0
        for index, row in df.iterrows():
            date = str(row['date'])
            if counter == 0:
                open = float(row['open'])
            if counter % self.steps == 0 and counter != 0:
                new_df = new_df.append({'date': date, 'low': low, 'high': high, 'open': open, 'close': close},
                                       ignore_index=True)
                high, low, close, open, date = 0, float('inf'), 0, 0, 0
                open = float(row['open'])
            close = float(row['close'])
            if float(row['high']) > high:
                high = float(row['high'])
            if float(row['low']) < low:
                low = float(row['low'])
            counter += 1
        print(new_df)


    def set_date(self, date):
        self.to_date = date


if __name__ == '__main__':
    with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
        local_config = json.load(local_config_file)
    with open(CONFIGURATION_FILE) as config_file:
        config = json.load(config_file)
    s = DataUtil(config, local_config, "TEST")
    s.set_date(datetime(2022, 7, 25, 17, 15))
    s.request_historical_data('BTC', 25)
