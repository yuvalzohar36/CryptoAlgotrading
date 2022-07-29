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

        if self.mode == "LIVE": # ??????
            bars = data

        # list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)
        for line in bars:  # Keep only first 5 columns, "date" "open" "high" "low" "close"
            del line[7:]

        bars.reverse()
        df = pd.DataFrame(bars, columns=["Open time", "Open", "High", "Low", "Close", "Volume",
                                         "Close time"])  # 2 dimensional tabular data
        new_df = pd.DataFrame(
            columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time"])  # 2 dimensional tabular data

        count = 0
        high, low, volume = 0, float('inf'), 0
        for index, row in df.iterrows():
            if float(row["High"]) > high:
                high = float(row["High"])
            if float(row["Low"]) < low:
                low = float(row["Low"])
            volume += float(row['Volume'])

            if index % self.steps == 0 and count != 0:
                open_time = row["Open time"]
                open = row["Open"]

                new_df = new_df.append(
                    {"Open time": open_time, "Open": open, "High": high, "Low": low, "Close": close, "Volume": volume,
                     "Close time": close_time},
                    ignore_index=True)

                close_time = row["Open time"]
                close = row["Open"]
                high, low, volume = 0, float('inf'), 0

            elif index % self.steps == 0 and count == 0:
                for index, row in df.iterrows():
                    close_time = row["Open time"]
                    close = row["Open"]
                    break
                high, low, volume = 0, float('inf'), 0
            count += 1
        return new_df.iloc[0:candles_count]

    def set_date(self, date):
        self.to_date = date

    def timestamp(self):
        return self.datetime().timestamp()

    def datetime(self):
        return self.to_date




if __name__ == '__main__':
    with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
        local_config = json.load(local_config_file)
    with open(CONFIGURATION_FILE) as config_file:
        config = json.load(config_file)
    s = DataUtil(config, local_config, "LIVE") #TEST / LIVE
    s.set_date(datetime(2022, 7, 25, 17, 15))
    x = s.request_historical_data('BTC', 25)
    for i in x.iterrows():
        print(i)