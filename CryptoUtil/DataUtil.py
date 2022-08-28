import random
from datetime import datetime, timedelta
import pandas as pd
import time
from TradeWallets.BinanceWallet import BinanceWallet
import threading
import firebase_admin
from firebase_admin import credentials, firestore

USERNAME = 'yuvalbadihi'
LOCAL_CONFIGURATION_FILE = "../Configurations/local_configuration.json"
CONFIGURATION_FILE = "../Configurations/configuration.json"


class DataUtil:
    def __init__(self, config, local_config, mode, start_date=None, end_date = None):
        self.config = config
        self.local_config = local_config
        self.mode = mode  # TEST, LIVE
        self.mins = self.config["TradeDetail"]["minutes"]  # append 'm'
        self.steps = self.config["TradeDetail"]["update_step_size"]
        self.to_date = start_date  # self.get_rand_date()
        self.end_date = end_date
        if start_date is not None:
            self.starting_date = self.to_date.date()
        self.moduls = self.load_moduls()
        self.running_indicators_amount = 0
        self.running_indicators_wrote_result_amount = 0
        if mode == 'LIVE':
            self.fb_db = self.init_FB(config["Paths"]["abs_path"] + config["Paths"]["FIREBASE_CREDENTIALS"])

        self.semaphores = {"MW_all_indi_finish_sem": threading.Semaphore(0),
                           "INDICATOR_write_to_db_sem": threading.Semaphore(),
                           "INDIRES_inc_counter_sem": threading.Semaphore(),
                           "process_firebase_writing_sem": threading.Semaphore()}

    def request_historical_data(self, symbol, candles_count):
        convert_symbol = symbol + "BUSD"
        client = self.moduls.get("Binance").client
        start_time = f"{self.steps * self.mins * candles_count + 60} minutes ago UTC"
        if self.mode == "LIVE":
            data = client.get_historical_klines(convert_symbol, str(self.mins) + 'm', start_time)
        else:
            temp_date = self.to_date + timedelta(days=1)
            from_date = self.to_date - timedelta(minutes=self.steps * self.mins * candles_count) - timedelta(days=2)
            data = client.get_historical_klines(convert_symbol, str(self.mins) + 'm',
                                                from_date.strftime("%d %b, %Y"),
                                                temp_date.strftime("%d %b, %Y"))

            new_data = []
            for i in data:
                new_data.append(i)
                if str(int(datetime.timestamp(self.to_date))) in str(i[0]):
                    break
            bars = new_data

        if self.mode == "LIVE":
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

    @staticmethod
    def get_rand_date():
        vals = [0, 15, 30, 45]
        return datetime(random.randint(2020, 2021), random.randint(1, 12),
                        random.randint(1, 28), random.randint(0, 23), vals[random.randint(0, 3)])

    def load_moduls(self):
        api_key = self.local_config["Binance"][USERNAME]["Details"]["api_key"]
        api_secret = self.local_config["Binance"][USERNAME]["Details"]["api_secret"]
        binance = BinanceWallet(api_key, api_secret, 0.1, USERNAME, self.config)
        dict = {"Binance": binance}
        return dict

    def currency_price(self, symbol):
        if symbol == "USDT" or symbol == "BUSD":
            return 1.0
        if self.mode == "LIVE":
            return self.moduls.get("Binance").currency_price(symbol)
        else:
            price = self.request_historical_data(symbol, 1)
            return float(price["Close"][0])

    def get_timestamp(self):
        if self.mode == "LIVE":
            return time.time()
        return self.to_date.timestamp()

    def get_datetime(self):
        if self.mode == "LIVE":
            return datetime.now()
        return self.to_date

    def get_path_for_assessments(self):
        if self.mode == "LIVE":
            return self.config["Paths"]["ASSESSMENT_DB_PATH"] + '.csv'
        return self.config["Paths"]["ASSESSMENT_DB_PATH_TEST"] + str(self.starting_date).replace('-', '_') + '.csv'

    def lock(self, sem_name):
        self.semaphores[sem_name].acquire()

    def unlock(self, sem_name):
        self.semaphores[sem_name].release()

    def get_data(self, symbol, val):
        return 69

    def init_FB(self, credentials_full_path):
        cred = credentials.Certificate(credentials_full_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db

    def get_fb_db(self):
        return self.fb_db
