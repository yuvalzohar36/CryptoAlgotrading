import threading
import time


class IndicatorResult:
    def __init__(self, indicator, coin, started_time, data_util, logger):
        self.coin = coin
        self.indicator = indicator
        self.result_setted = False
        self.result = None  # 0--> INFINITY
        self.credit = 1
        self.sem_credit_updated = threading.Semaphore(0)
        self.started_time = started_time
        self.timer = 0
        self.data_util = data_util
        self.logger = logger

    def set_result_setted(self):
        self.result_setted = True

    def set_result(self, result):
        self.result = result
        self.set_result_setted()
        self.timer = time.time() - self.started_time
        self.logger.info(f"{self.coin.symbol} result is: {result}")
        self.data_util.lock('INDIRES_inc_counter_sem')
        self.data_util.running_indicators_wrote_result_amount += 1
        if self.data_util.running_indicators_wrote_result_amount >= self.data_util.running_indicators_amount:
            self.data_util.unlock('MW_all_indi_finish_sem')
            self.data_util.running_indicators_wrote_result_amount = 0
        self.data_util.unlock('INDIRES_inc_counter_sem')


    def call_back_credit_result(self, new_credit):
        self.credit = new_credit
