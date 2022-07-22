import time
import threading
import logging
from os.path import exists
from Coins import CryptoCoin as CC
from Coins.ResultForWM import ResultForWM
from TradeWallets.BinanceWallet import BinanceWallet
import importlib
import pandas as pd
import datetime as dt


class CoinsManager:
    def __init__(self, config, local_config):
        self.binance_module = self.binance_connect(local_config, config)
        self.config = config
        self.local_config = local_config
        self.coins, self.coins_indicators = self.init_coins()
        self.current_indicators_threads = {}
        self.assessment_df = self.init_weights_assessments(self.config["Paths"]["abs_path"] + self.config["Paths"]["ASSESSMENT_DB_PATH"],
                                                           ["Coin", "Indicator", "Result", "Credit", "PrevPrice", "UpdateTime"])
        self.indicators_loggers = self.init_all_loggers()
        self.semaphore = threading.Semaphore()
        self.activate_all_indicators()
        time.sleep(5)

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
                coins[coin] = CC.CryptoCoin(coin, self.local_config, self.config)
        return coins, coins_indicators

    def append_new_thread(self, indicator, thread):
        self.current_indicators_threads[indicator] = thread

    def recv_indicator_results(self, symbol):
        results = []
        for indi in self.coins_indicators[symbol]:
            results.append(indi.get_results())
            indi_credit = self.get_indi_val(indi, symbol, 'Credit')
            indi_result = self.get_indi_val(indi, symbol, 'Result')
            new_indi_credit = self.credit_distributor(indi, symbol, indi_credit, indi_result)
            indi.get_results().call_back_credit_result(new_indi_credit)
          #  indi.get_results().sem_credit_updated.release()
            indi.write_val_to_DB(type(indi).__name__, new_indi_credit, 'Credit')
            indi.write_val_to_DB(type(indi).__name__, self.binance_module.currency_price(symbol), 'PrevPrice')
            indi.write_val_to_DB(type(indi).__name__, time.time(), 'UpdateTime')
            indi.write_val_to_DB(type(indi).__name__, None, 'Result')  # writes to database

        return results

    def join_thread(self, indicator):
        self.current_indicators_threads[indicator].join()

    def stats(self, symbol):
        buy_credit = 0
        sell_credit = 0
        hold_credit = 0
        buy_count = 0
        sell_count = 0
        hold_count = 0
        self.recv_indicator_results(symbol)
        for indi in self.coins_indicators[symbol]:
         #   if not self.check_if_result_valid(indi, symbol):
          #      continue

            indi_credit = self.get_indi_val(indi, symbol, 'Credit')
            indi_result = self.get_indi_val(indi, symbol, 'Result')
            if indi_result == 'BUY':
                buy_credit += indi_credit
                buy_count += 1

            elif indi_result == 'SELL':
                sell_credit += indi_credit
                sell_count += 1

            elif indi_result == 'HOLD':
                hold_credit += indi_credit
                hold_count += 1

        return ResultForWM([self.coins.get(symbol), buy_credit, sell_credit,
                            hold_credit, buy_count, sell_count, hold_count, dt.datetime.now()])

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

    @staticmethod
    def init_weights_assessments(full_path, col):
        if not exists(full_path):
            assessment_df = pd.DataFrame(
                columns=col)
            assessment_df.to_csv(full_path, index=False)
        else:
            assessment_df = pd.read_csv(full_path)
        return assessment_df

    @staticmethod
    def get_indi_val(indi, symbol, title):
        return indi.get_indi_val(symbol, type(indi).__name__, title)

    def credit_distributor(self, indi, symbol, indi_credit, indi_result):
        curr_price = self.binance_module.currency_price(symbol)
        prev_price = self.get_indi_val(indi, symbol, 'PrevPrice')

        if not self.check_if_result_valid(indi, symbol):
            return indi_credit

        if prev_price is None:
            return indi_credit
        score = (curr_price/prev_price)
        diff = abs(1-score)*indi_credit

        if indi_result == 'BUY' and score > 0:
            return indi_credit + diff

        elif indi_result == 'BUY' and score < 0:
            return indi_credit - diff

        elif indi_result == 'SELL' and score < 0:
            return indi_credit + diff

        elif indi_result == 'SELL' and score > 0:
            return indi_credit - diff

        return indi_credit

    @staticmethod
    def binance_connect(local_config, config):
        USERNAME = 'yuvalbadihi'
        api_key = local_config["Binance"][USERNAME]["Details"]["api_key"]
        api_secret = local_config["Binance"][USERNAME]["Details"]["api_secret"]
        binance_module = BinanceWallet(api_key, api_secret, 0.1, USERNAME, config)
        return binance_module

    def check_if_result_valid(self, indi, symbol):
        update_time = self.get_indi_val(indi, symbol, 'UpdateTime')
        miss = 1.25
        if update_time + (self.config["TradeDetail"]["update_step_size"]*self.config["TradeDetail"]["minutes"]*60)*miss < time.time():
            return False

        elif time.time() < update_time + (self.config["TradeDetail"]["update_step_size"]*self.config["TradeDetail"]["minutes"]*60)*(2-miss):
            return False

        return True

    def receive_coins(self):
        return self.coins











