import time
from threading import Thread
import TradeWallets.BinanceWallet as BW
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web
from Indicators.Indicator import Indicator

import datetime as dt


class EMAIndicator(Indicator):
    def __init__(self):
        super().__init__()
        self.connection = Indicator.connect(self.api_key, self.api_secret)
        self.results = [0.0, 0.0]
        self.init_logger(type(self).__name__, self.config)

    def execute(self, args):
        self.args = args
        t1 = Thread(target=self.check, args=())
        t1.start()
        t1.join()

    def check(self):
        symbol = self.args
        start = dt.datetime(2022, 1, 1)
        end = dt.datetime.now()
        against_currency = "USDT"

        df = web.DataReader(symbol, 'yahoo', start, end)

        ema = self.calculate_ema(df['Close'], 10)

        price_X = np.arange(df.shape[0])  # Creates array [0, 1, 2, 3, ..., df.shape[0]]
        ema_X = np.arange(10, df.shape[0] + 1)  # Creates array [10, 11, 12, 13, ..., df.shape[0]+1]
        # We start at 10, because we use the first 10 values to calculate the SMA,
        # then we calculate EMA form the 11th value

        print(ema)

    def get_results(self):
        return self.results

    def calculate_ema(self, prices, days, smoothing=2):
        ema = [sum(prices[:days]) / days]
        for price in prices[days:]:
            ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
        return ema

x = EMAIndicator()
x.execute("BTC")