import time
import threading
import logging
from os.path import exists
from apscheduler.schedulers.background import BackgroundScheduler
from Coins import CryptoCoin as CC
from Coins.ResultForWM import ResultForWM
import importlib
import pandas as pd
import datetime as dt


class CoinsManager:
    def __init__(self,data_util):
        self.config = data_util.config
        self.local_config = data_util.local_config
        self.pickup_duration = float(self.config["TradeDetail"]["update_step_size"]) * float(
            self.config["TradeDetail"]["minutes"])*60
        self.scheduler = BackgroundScheduler()
        self.data_util = data_util
        self.coinsDB = self.init_coins_db(self.config["Paths"]["abs_path"] + self.config["Paths"]["COINS_DB_PATH"])
        self.coins, self.coins_indicators = self.init_coins()
        self.current_indicators_threads = {}
        self.assessment_df = self.init_weights_assessments(
            self.config["Paths"]["abs_path"] + self.config["Paths"]["ASSESSMENT_DB_PATH"],
            ["Coin", "Indicator", "Result", "Credit", "PrevPrice", "UpdateTime"])
        self.indicators_loggers = self.init_all_loggers()
        self.semaphore = threading.Semaphore()
        self.activate_all_indicators()

        # here update all the coinsDB data

        self.coinsDB.to_csv(self.config["Paths"]["abs_path"] + self.config["Paths"]["COINS_DB_PATH"], index=False)

    def schedule_all_indicators_jobs(self):
        self.scheduler = BackgroundScheduler()
        for coin in self.coins:
            self.coins[coin].attributes_refresh()
        for coin in self.config["Coins"]:
            if self.config["Coins"][coin]["Mode"] == "ON":
                for indicator in self.coins_indicators[coin]:
                    delta_time = self.pickup_duration - float(
                        self.config["Indicators"][type(indicator).__name__]["DURATION"])
                    indicators_timestamp = dt.datetime.now().timestamp() + delta_time - int(
                        self.config["SAFE_TIME_OFFSET"])
                    dt_obj = dt.datetime.fromtimestamp(indicators_timestamp)
                    self.add_scheduler_job(self.indicator_activate, [indicator, self.coins[coin]], dt_obj)
        self.scheduler.start()

    def add_scheduler_job(self, func, args, start_time):
        self.scheduler.add_job(
            func=func,
            args=args,
            trigger="date",
            run_date=start_time,
            name="new_indicator_job",
            misfire_grace_time=600,
            coalesce=True,
        )

    @staticmethod
    def indicator_activate(indicator, coin_instance):
        args = [coin_instance]
        indicator.execute(args)

    def activate_all_indicators(self):
        MAIN_PATH = self.config["Paths"]["MAIN_INDICATORS_PATH"]
        for coin in self.coins.keys():
            for indicator in self.config["Indicators"].keys():
                if self.config["Indicators"][indicator]["MODE"] == "OFF":
                    continue
                indicator_dict = self.config["Indicators"][indicator]
                module = importlib.import_module(MAIN_PATH + indicator_dict["MODULE_PATH"])
                class_ = getattr(module, indicator_dict["MODULE_PATH"])
                current_indicator = class_(self, self.indicators_loggers[indicator], self.assessment_df,
                                           self.semaphore, self.data_util)
                # self.indicator_activate(current_indicator, self.coins[coin])
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
                coins[coin] = CC.CryptoCoin(coin, self.local_config, self.config, self.coinsDB)
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
            indi.write_val_to_DB(type(indi).__name__, self.data_util.currency_price(symbol), 'PrevPrice')
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
            # if not self.check_if_result_valid(indi, symbol):
            #     continue

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
        curr_price = self.data_util.currency_price(symbol)
        prev_price = self.get_indi_val(indi, symbol, 'PrevPrice')

        # if not self.check_if_result_valid(indi, symbol):
        #     return indi_credit

        if prev_price is None:
            return indi_credit
        score = (curr_price / prev_price)
        diff = abs(1 - score) * indi_credit

        if indi_result == 'BUY' and score > 0:
            return indi_credit + diff

        elif indi_result == 'BUY' and score < 0:
            return indi_credit - diff

        elif indi_result == 'SELL' and score < 0:
            return indi_credit + diff

        elif indi_result == 'SELL' and score > 0:
            return indi_credit - diff

        return indi_credit

    def check_if_result_valid(self, indi, symbol):
        update_time = self.get_indi_val(indi, symbol, 'UpdateTime')
        miss = 1.25
        if update_time + (self.config["TradeDetail"]["update_step_size"] * self.config["TradeDetail"][
            "minutes"] * 60) * miss < time.time():
            return False

        elif time.time() < update_time + (
                self.config["TradeDetail"]["update_step_size"] * self.config["TradeDetail"]["minutes"] * 60) * (
                2 - miss):
            return False

        return True

    def receive_coins(self):
        return self.coins

    def init_coins_db(self, full_path):
        if not exists(full_path):
            columns = ['Coin', 'MaxAttributeVal', 'Stability', 'Security', 'Scalability', 'Supply', 'Decentralisation',
                       'Demand', 'Usefulness', 'Backup_Date']
            df = pd.DataFrame(columns=columns)
            for coin in self.config["Coins"]:
                if self.config["Coins"][coin]["Mode"] == "ON":
                    df.loc[len(df.index)] = [coin, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            df.to_csv(full_path, index=False)
        df = pd.read_csv(full_path)
        return df
