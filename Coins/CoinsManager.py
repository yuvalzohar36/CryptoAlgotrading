import time
from threading import Thread
import threading
import logging
from os.path import exists
from Coins import CryptoCoin as CC
from Indicators.IndicatorsImplements.MAIndicator import MAIndicator as MA
import importlib
import pandas as pd


class CoinsManager:
    def __init__(self, config):
        self.config = config
        self.coins, self.coins_indicators = self.init_coins()
        self.current_indicators_threads = {}
        self.assessment_df = self.init_weights_assessments(self.config["Paths"]["abs_path"] + self.config["Paths"]["ASSESSMENT_DB_PATH"],["Coin", "Indicator", "Result", "Credit"])
        self.coins_round_df = self.init_weights_assessments(self.config["Paths"]["abs_path"] + self.config["Paths"]["COINS_ROUND_DATA_DB_PATH"],["Coin", "OldPrice"])
        self.indicators_loggers = self.init_all_loggers()
        self.semaphore = threading.Semaphore()
        self.activate_all_indicators()
        time.sleep(2)
        print("done!")
    #    self.assessment_df.to_csv(f"{config['Paths']['abs_path'] + config['Paths']['ASSESSMENT_DB_PATH']}", index=False)  # upgrade

    @staticmethod
    def indicator_activate(indicator, coin_instance):
        args = [coin_instance]
        indicator.execute(args)

    def activate_all_indicators(self):
        MAIN_PATH = self.config["Paths"]["MAIN_INDICATORS_PATH"]
        for coin in self.coins.keys():
            for indicator in self.config["Indicators"].keys():
                    indicator_dict = self.config["Indicators"][indicator]
                    module = importlib.import_module(MAIN_PATH + indicator_dict["MODULE_PATH"])
                    class_ = getattr(module, indicator_dict["MODULE_PATH"])
                    current_indicator = class_(self, self.indicators_loggers[indicator], self.assessment_df,
                                               self.semaphore)
                    self.indicator_activate(current_indicator, self.coins[coin])
                    self.coins_indicators[coin].append(current_indicator)

    def refresh_all_indicators(self):

        for i in self.coins_indicators.keys():
            indi_lst = self.coins_indicators.get(i)
            for indi in indi_lst:
                indi.execute([self.coins[i]])
          #  for x in self.coins_indicators.values()[i]:
           #     x.execute([self.coins[coin]])

    def init_all_loggers(self):
        indicators_loggers = {}
        for indicator in self.config["Indicators"].keys():
            indicators_loggers[indicator] = CoinsManager.init_logger(indicator, self.config)
        return indicators_loggers

    def init_coins(self):
        coins = {}
        coins_indicators = {}
        for coin in self.config["Coins"]:
            if self.config["Coins"][coin]["Mode"] == "ON":
                coins_indicators[coin] = []
                coins[coin] = CC.CryptoCoin(coin)
        return coins, coins_indicators

    def append_new_thread(self, indicator, thread):
        self.current_indicators_threads[indicator] = thread

    def recv_indicator_results(self, symbol):
        results = []
        for indi in self.coins_indicators[symbol]:
            results.append(indi.get_results())
            indi.write_result_to_DB(type(indi).__name__)
        return results

    def join_thread(self, indicator):
        self.current_indicators_threads[indicator].join()

    def result_per_coin(self, symbol):
        lst = []
        for result in self.recv_indicator_results(symbol):
            if result.result_setted:
                lst.append(result.result)
        lst.append("NEED TO DO A SUM IN result_per_coin")
        return lst

    @staticmethod
    def init_logger(logger_name, config_file):
        # Create a custom logger
        logger_path = config_file["Paths"]["abs_path"] + config_file["Paths"]["logger_folder"] + config_file["Paths"][
            "indicators_logs_path"]
        logger_full_path = logger_path + logger_name + ".log"
        logger = logging.getLogger(name=logger_name)
        log_formatter = logging.Formatter(config_file["Logger"]["wallet_log_format"])
        log_file_handler = logging.FileHandler(
            logger_full_path, mode=config_file["Logger"]["wallet_log_filemode"]
        )
        log_file_handler.setFormatter(log_formatter)
        logger.addHandler(log_file_handler)
        logger.setLevel(config_file["Logger"]["wallet_log_setting_level"])
        logger.info("Initialize logger")
        return logger

    def init_weights_assessments(self,full_path,col):
        if not exists(full_path):
            assessment_df = pd.DataFrame(
                columns=col)
            assessment_df.to_csv(full_path, index=False)
        else:
            assessment_df = pd.read_csv(full_path)
        return assessment_df


