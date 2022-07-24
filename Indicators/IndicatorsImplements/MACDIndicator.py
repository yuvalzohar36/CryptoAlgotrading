import time
import warnings
import numpy as np
from Indicators.Indicator import Indicator
import pandas as pd


class MACDIndicator(Indicator):
    def __init__(self, coin_manager, logger, assessment_df, semaphore):
        super().__init__(coin_manager, logger, assessment_df, semaphore)
        self.candles_measure = 10
        self.diff = 1.0
        self.bad_credit = 0.9
        self.steps = super().get_config()["TradeDetail"]["update_step_size"]
        self.mins = super().get_config()["TradeDetail"]["minutes"]
        self.coin = None
        self.client = super().get_binance_module().client

    def run(self, args):
        self.coin = args[0]
        warnings.filterwarnings("ignore")
        self.macd_trade_logic()

    def get_data_frame(self):
        starttime = '1 day ago UTC'
        interval = self.mins
        bars = self.client.get_historical_klines(self.coin.symbol + "USDT", str(interval) + 'm', starttime)
        for line in bars:  # Keep only first 5 columns, "date" "open" "high" "low" "close"
            del line[5:]
        df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])  # 2 dimensional tabular data
        new_df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close'])  # 2 dimensional tabular data
        high, low, close, open, date = 0, float('inf'), 0, 0, 0
        counter = 0
        for index, row in df.iterrows():
            date = str(row['date'])
            if counter == 0:
                open = float(row['open'])
            if counter % self.steps == 0 and counter != 0:
                new_df = new_df.append({'date': date, 'low': low, 'high': high, 'open': open, 'close': close},
                                       ignore_index=True)
                high, low, close, open, date = 0, float('inf'), 0, 0, 0
                open = float(row['open'])
            close = float(row['close'])
            if float(row['high']) > high:
                high = float(row['high'])
            if float(row['low']) < low:
                low = float(row['low'])
            counter += 1
        return new_df

    def macd_trade_logic(self):
        symbol_df = self.get_data_frame()
        shortEMA = symbol_df['close'].ewm(span=12, adjust=False).mean()
        longEMA = symbol_df['close'].ewm(span=26, adjust=False).mean()

        # Calculate MACD and signal line
        MACD = shortEMA - longEMA
        signal = MACD.ewm(span=9, adjust=False).mean()
        symbol_df['MACD'] = MACD
        symbol_df['signal'] = signal

        symbol_df['Trigger'] = np.where(symbol_df['MACD'] > symbol_df['signal'], 1, 0)
        symbol_df['Position'] = symbol_df['Trigger'].diff()

        # Add buy and sell columns
        symbol_df['Buy'] = np.where(symbol_df['Position'] == 1, symbol_df['close'], np.NaN)
        symbol_df['Sell'] = np.where(symbol_df['Position'] == -1, symbol_df['close'], np.NaN)
        symbol_df.set_index('date', inplace=True)
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
