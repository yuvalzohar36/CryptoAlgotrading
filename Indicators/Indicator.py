import json
import logging
from abc import ABC, abstractmethod

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

    @abstractmethod
    def execute(self, args):
        pass

    @staticmethod
    def connect(api_key, api_secret):
        return Client(api_key, api_secret)

    @abstractmethod
    def get_results(self):
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
