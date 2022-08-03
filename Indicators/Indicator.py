from abc import ABC, abstractmethod
from threading import Thread
from Indicators import IndicatorResult as IR
import pandas as pd
import time

LOCAL_CONFIGURATION_FILE = "../Configurations/local_configuration.json"
CONFIGURATION_FILE = "../Configurations/configuration.json"
USERNAME = "yuvalbadihi"


class Indicator(ABC):
    def __init__(self, coin_manager, logger, assessment_df, data_util):
        self.data_util = data_util
        self.local_config = data_util.local_config
        self.config = data_util.config
        self.logger = logger
        self.coin_manager = coin_manager
        self.assessment_df = assessment_df
        self.result = None
        self.args = None

    def execute(self, args):
        self.result = IR.IndicatorResult(self, args[0], time.time(), self.data_util, self.logger)
        self.args = args
        t1 = Thread(target=self.run, args=[self.args])
        self.logger.info(f"Execute for Symbol {self.args[0].symbol}")
        self.coin_manager.append_new_thread(self, t1)
        t1.start()

    def get_results(self):
        return self.result

    @abstractmethod
    def run(self, args):
        pass

    def find_row(self, coin, indicator_name):
        for index, row in self.assessment_df.iterrows():
            if row["Coin"] == coin and row["Indicator"] == indicator_name:
                return index
        return -1

    def add_row(self, coin, indicator_name):
        new_line = {'Coin': coin, 'Indicator': indicator_name, 'Result': "HOLD", 'Credit': 1,
                    'PrevPrice': self.data_util.currency_price(coin), "UpdateTime": self.data_util.get_timestamp()}
        self.assessment_df = self.assessment_df.append(new_line, ignore_index=True)
        return self.find_row(coin, indicator_name)

    def change_row_val(self, coin, indicator_name, val, title):
        res = self.find_row(coin, indicator_name)
        if res == -1:
            res = self.add_row(coin, indicator_name)
        self.assessment_df.loc[[res], [title]] = val
        full_path = self.config["Paths"]["abs_path"] + self.config["Paths"][self.data_util.get_path_for_assessments()]
        self.assessment_df.to_csv(full_path, index=False)

    def write_val_to_DB(self, indicator_name, val, title):
        if title == 'Result':
            if self.result.result_setted:
                val = self.result.result
            else:
                val = 'HOLD'
        self.data_util.lock("INDICATOR_write_to_db_sem")
        full_path = self.config["Paths"]["abs_path"] + self.config["Paths"][self.data_util.get_path_for_assessments()]
        self.assessment_df = pd.read_csv(full_path)
        coin = self.args[0].symbol
        self.change_row_val(coin, indicator_name, val, title)
        self.data_util.unlock("INDICATOR_write_to_db_sem")

    def get_indi_val(self, coin, indicator_name, title):
        self.data_util.lock("INDICATOR_write_to_db_sem")
        full_path = self.config["Paths"]["abs_path"] + self.config["Paths"][self.data_util.get_path_for_assessments()]
        self.assessment_df = pd.read_csv(full_path)
        row = self.find_row(coin, indicator_name)
        if row == -1:
            self.data_util.unlock("INDICATOR_write_to_db_sem")
            return 1
        self.data_util.unlock("INDICATOR_write_to_db_sem")
        return self.assessment_df[title][row]

    def my_credit(self):
        return self.result.credit

    def sem_credit_updated(self):
        return self.result.sem_credit_updated

    def get_config(self):
        return self.config

    def get_data_util(self):
        return self.data_util

    def get_logger(self):
        return self.logger

