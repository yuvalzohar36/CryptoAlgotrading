import json
import logging
from abc import ABC, abstractmethod
from threading import Thread
from Indicators import IndicatorResult as IR

from binance import Client

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

    def execute(self, args):
        self.result = IR.IndicatorResult(self, args[0], args[1])
        self.args = args
        t1 = Thread(target=self.check, args=[self.args])
        self.logger.info(f"Execute for Symbol {self.args[0].symbol}")
        self.coin_manager.append_new_thread(self, t1)
        t1.start()

    def get_results(self):
        self.logger.info(f"Current result for symbol {self.args[0].symbol} is: ")
        self.logger.info(
            f"Percent result is: {self.result.percent_result}")
        return self.result

    @staticmethod
    def connect(api_key, api_secret):
        return Client(api_key, api_secret)

    @abstractmethod
    def check(self, args):
        pass

    def lock(self):
        self.semaphore.acquire()

    def unlock(self):
        self.semaphore.release()

    def write_result_to_DB(self, indicator_name):
        self.lock()
        coin = self.args[0].symbol
        res = self.result.percent_result
        interval = self.args[1]
        column = "Current_" + interval
        self.change_row_val(coin, indicator_name, res, column)
        self.unlock()

    def change_row_val(self, coin, indicator_name, val, col):
        for index, row in self.assessment_df.iterrows():
            if row["Coin"] == coin and row["Indicator"] == indicator_name:
                self.assessment_df.loc[index, col] = val
