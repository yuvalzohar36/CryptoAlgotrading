import threading

class IndicatorResult:
    def __init__(self, indicator, coin):
        self.coin = coin
        self.indicator = indicator
        self.result_setted = False
        self.result = None  # 0--> INFINITY
        self.credit = 1
        self.sem_credit_updated = threading.Semaphore(0)


    def set_result_setted(self):
        self.result_setted = True

    def set_result(self, result):
        self.result = result
        self.set_result_setted()

    def call_back_credit_result(self, new_credit):
        self.credit = new_credit

