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
    def __init__(self, coin_manager):
        with open(LOCAL_CONFIGURATION_FILE) as local_config_file:
            self.local_config = json.load(local_config_file)
        with open(CONFIGURATION_FILE) as config_file:
            self.config = json.load(config_file)
        self.api_key = self.local_config["Binance"][USERNAME]["Details"]["api_key"]
        self.api_secret = self.local_config["Binance"][USERNAME]["Details"]["api_secret"]
        self.coin_manager = coin_manager

    def execute(self, args):
        self.result = IR.IndicatorResult(self, args[0])
        self.args = args
        t1 = Thread(target=self.check, args=(self.args))
        self.coin_manager.append_new_thread(self, t1)
        t1.start()

    def get_results(self):
        return self.result

    @staticmethod
    def connect(api_key, api_secret):
        return Client(api_key, api_secret)

    @abstractmethod
    def check(self, args):
        pass

    def init_logger(self, logger_name, config_file):
        # Create a custom logger
        logger_path = config_file["Paths"]["abs_path"] + config_file["Paths"]["logger_folder"] + config_file["Paths"][
            "indicators_logs_path"]
        logger_full_path = logger_path + logger_name + ".log"
        self.logger = logging.getLogger(name=logger_name)
        log_formatter = logging.Formatter(config_file["Logger"]["wallet_log_format"])
        log_file_handler = logging.FileHandler(
            logger_full_path, mode=config_file["Logger"]["wallet_log_filemode"]
        )
        log_file_handler.setFormatter(log_formatter)
        self.logger.addHandler(log_file_handler)
        self.logger.setLevel(config_file["Logger"]["wallet_log_setting_level"])
        self.logger.info("Initialize logger")
