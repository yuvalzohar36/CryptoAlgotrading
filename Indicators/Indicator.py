import json
from abc import ABC, abstractmethod
from TradeWallets.BinanceWallet import BinanceWallet
from threading import Thread
from Indicators import IndicatorResult as IR
from binance import Client
import pandas as pd

LOCAL_CONFIGURATION_FILE = "../Configurations/local_configuration.json"
CONFIGURATION_FILE = "../Configurations/configuration.json"
USERNAME = "yuvalbadihi"


class Indicator(ABC):
    def __init__(self, coin_manager, logger, assessment_df, semaphore):
        with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
            self.local_config = json.load(local_config_file)
        with open(CONFIGURATION_FILE) as config_file:
            self.config = json.load(config_file)
        self.logger = logger
        self.api_key = self.local_config["Binance"][USERNAME]["Details"]["api_key"]
        self.api_secret = self.local_config["Binance"][USERNAME]["Details"]["api_secret"]
        self.coin_manager = coin_manager
        self.assessment_df = assessment_df
        self.semaphore = semaphore
        self.binance_module = coin_manager.binance_module

    def execute(self, args):
        self.result = IR.IndicatorResult(self, args[0])
        self.args = args
        t1 = Thread(target=self.run, args=[self.args])
        self.logger.info(f"Execute for Symbol {self.args[0].symbol}")
        self.coin_manager.append_new_thread(self, t1)
        t1.start()

    def get_results(self):
        self.logger.info(f"Current result for symbol {self.args[0].symbol} is: ")
        self.logger.info(
            f"Percent result is: {self.result.result}")
        return self.result

    @staticmethod
    def connect(api_key, api_secret):
        return Client(api_key, api_secret)

    @abstractmethod
    def run(self, args):
        pass

    def lock(self):
        self.semaphore.acquire()

    def unlock(self):
        self.semaphore.release()


    def find_row(self, coin, indicator_name):
        for index, row in self.assessment_df.iterrows():
            if row["Coin"] == coin and row["Indicator"] == indicator_name:
                return index
        return -1

    def add_row(self, coin, indicator_name):
        new_line = {'Coin': coin, 'Indicator': indicator_name, 'Result': "HOLD", 'Credit': 1, 'PrevPrice': self.binance_module.currency_price(coin)}
        self.assessment_df = self.assessment_df.append(new_line, ignore_index=True)
        return self.find_row(coin, indicator_name)

    def change_row_val(self, coin, indicator_name, val, title):
        res = self.find_row(coin,indicator_name)
        if res == -1:
            res = self.add_row(coin, indicator_name)
        self.assessment_df.loc[[res], [title]] = val
        full_path = self.config["Paths"]["abs_path"] + self.config["Paths"]["ASSESSMENT_DB_PATH"]
        self.assessment_df.to_csv(full_path, index=False)

    def write_val_to_DB(self, indicator_name, val, title):
        if title == 'Result':
            if self.result.result_setted:
                 val = self.result.result
            else:
                 val = 'HOLD'
        self.lock()
        full_path = self.config["Paths"]["abs_path"] + self.config["Paths"]["ASSESSMENT_DB_PATH"]
        self.assessment_df = pd.read_csv(full_path)
        coin = self.args[0].symbol
        self.change_row_val(coin, indicator_name, val, title)
        self.unlock()

    def get_indi_val(self, coin, indicator_name, title):
        self.lock()
        full_path = self.config["Paths"]["abs_path"] + self.config["Paths"]["ASSESSMENT_DB_PATH"]
        self.assessment_df = pd.read_csv(full_path)
        row = self.find_row(coin, indicator_name)
        if row == -1:
            self.unlock()
            return 1
        self.unlock()
        return self.assessment_df[title][row]

    def get_binance_module(self):
        return self.binance_module

    def my_credit(self):
        return self.result.credit

    def sem_credit_updated(self):
        return self.result.sem_credit_updated

    def get_config(self):
        return self.config









