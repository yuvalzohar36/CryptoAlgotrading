from binance.client import Client
import pandas as pd


class Wallet:
    def __init__(self, api_key, api_secret, convertor, risk):
        self.api_key, self.api_secret = Wallet.making_api_key(api_key, api_secret)
        self.client = self.connect()
        self.convertor = convertor
        self.risk = risk  # number between 0 -> 1

    def buy(self, from_currency, to_currency, type_market, quantity):
        if from_currency == to_currency:
            return 0

        if from_currency != "USDT":
            symbol = Wallet.get_symbol(from_currency, "USDT")
            min_qty, step_size = self.min_qty_step_size(from_currency)
            if min_qty is None or step_size is None:
                return 0
            optimal_quantity = round((quantity // min_qty) * step_size, 8)
            if self.is_valid_lot_size(optimal_quantity, min_qty):
                self.client.create_order(symbol=symbol, side="SELL", type=type_market, quantity=optimal_quantity)
            else:
                return 0
        else:
            optimal_quantity = quantity
        if to_currency != "USDT":
            quantity = optimal_quantity * float(self.currency_price(from_currency))
            new_quantity = quantity / float(self.currency_price(to_currency))
            symbol = Wallet.get_symbol(to_currency, "USDT")
            min_qty, step_size = self.min_qty_step_size(to_currency)
            if not (min_qty is None or step_size is None):
                optimal_quantity = round((new_quantity // min_qty) * step_size, 8)
                if self.is_valid_lot_size(optimal_quantity, min_qty):
                    self.client.create_order(symbol=symbol, side="BUY", type=type_market, quantity=optimal_quantity)
                else:
                    return 0
        return quantity

    def currency_price(self, currency):
        if currency == "USDT":
            return 1
        df = pd.DataFrame(self.client.get_all_tickers())
        df = df[df['symbol'] == Wallet.get_symbol(currency, "USDT")]
        return df['price'].iloc[0]

    def connect(self):
        return Client(self.api_key, self.api_secret)

    @staticmethod
    def get_symbol(from_currency, to_currency):
        return from_currency + to_currency

    @staticmethod
    def making_api_key(api_key, api_secret):
        return api_key, api_secret

    def get_products(self):
        data = self.client.get_products()['data']
        symbols_list = []
        for symbol in data:
            symbols_list.append(symbol['s'])
        return symbols_list

    def relevant_account_info(self):  # returns df of only relevant coins (free>0)
        info_df = pd.DataFrame(self.client.get_account()['balances'])
        info_df['free'] = info_df['free'].apply(lambda x: float(x))  # change string to float
        return info_df.loc[info_df['free'] > 0]

    def abort(self, percent):  # percent 0->1
        df = self.relevant_account_info()
        total_investment = 0
        for data in df.iterrows():
            free_quantity = float(data[1]['free']) * percent
            total_investment += self.buy(data[1]['asset'], "USDT", "MARKET", free_quantity)
        return total_investment

    def is_valid_lot_size(self, optimal_quantity, min_qty):  # (quantity-minQty) % stepSize == 0
        return min_qty <= optimal_quantity

    def min_qty_step_size(self, currency):
        symbol_info = self.client.get_symbol_info(Wallet.get_symbol(currency, "USDT"))
        if symbol_info is None:
            return None, None
        return float(symbol_info['filters'][2]['minQty']), float(symbol_info['filters'][2]['stepSize'])

    def get_all_prices(self):
        return self.client.get_all_tickers()

    def get_currency_balance(self, currency):
        return float(self.client.get_asset_balance(asset=currency)['free'])

    def invest_on_currency(self, currency, percent):
        abort = self.abort(percent)
        cur_price = float(self.currency_price(currency))
        total_investment = abort * cur_price
        ans = self.buy("USDT",currency , "MARKET", total_investment)
        return ans
