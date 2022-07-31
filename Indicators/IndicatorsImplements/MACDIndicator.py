import time
import warnings
import numpy as np
from Indicators.Indicator import Indicator
import pandas as pd


class MACDIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, semaphore, data_util):
        super().__init__(coin_manager, logger, assessment_df, semaphore, data_util)
        self.candles_measure = 10
        self.diff = 1.0
        self.bad_credit = 0.9
        self.steps = super().get_config()["TradeDetail"]["update_step_size"]
        self.mins = super().get_config()["TradeDetail"]["minutes"]
        self.coin = None
        self.client = super().get_data_util().moduls.get("Binance").client

    def run(self, args):
        self.coin = args[0]
        warnings.filterwarnings("ignore")
        self.macd_trade_logic()

    def get_data_frame(self):
        return super().get_data_util().request_historical_data(self.coin.symbol, self.candles_measure)

    def macd_trade_logic(self):
        symbol_df = self.get_data_frame()
        # calculate short and long EMA mostly using close values
        shortEMA = symbol_df['Close'].ewm(span=12, adjust=False).mean()
        longEMA = symbol_df['Close'].ewm(span=26, adjust=False).mean()

        # Calculate MACD and signal line
        MACD = shortEMA - longEMA
        signal = MACD.ewm(span=9, adjust=False).mean()
        symbol_df['MACD'] = MACD
        symbol_df['signal'] = signal
        symbol_df['Trigger'] = np.where(symbol_df['MACD'] > symbol_df['signal'], 1, 0)
        symbol_df['Position'] = symbol_df['Trigger'].diff()

        # Add buy and sell columns
        symbol_df['Buy'] = np.where(symbol_df['Position'] == 1, symbol_df['Close'], np.NaN)
        symbol_df['Sell'] = np.where(symbol_df['Position'] == -1, symbol_df['Close'], np.NaN)
        symbol_df.set_index('Open time', inplace=True)
        symbol_df.index = pd.to_datetime(symbol_df.index, unit='ms')
        buy_sell_list = symbol_df['Position'].tolist()
        self.buy_or_sell(symbol_df, buy_sell_list)

    def buy_or_sell(self, df, buy_sell_list):
        for index, value in enumerate(buy_sell_list):
            current_price = self.client.get_symbol_ticker(symbol=self.coin.symbol + "USDT")
            if value == 1.0:  # signal to buy
                if float(current_price['price']) < float(df['Buy'][index]):
                    self.result.set_result('BUY')

            elif value == -1.0:  # signal to sell
                if float(current_price['price']) > float(df['Sell'][index]):
                    self.result.set_result('SELL')
            else:
                self.result.set_result('HOLD')
