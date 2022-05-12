import pprint

from binance.client import Client


class Wallet:
    def __init__(self, api_key, api_secret,convertor, risk):
        self.api_key, self.api_secret = Wallet.making_api_key(api_key, api_secret)
        self.client = self.connect()
        self.convertor = convertor
        self.risk = risk # number between 0 -> 1

    def buy(self, from_currency, to_currency, type_market, quantity):
        symbol = Wallet.get_symbol(from_currency, to_currency)
        return self.client.create_order(symbol=symbol, side="BUY", type=type_market, quantity=quantity)

    def sell(self, from_currency, to_currency, type_market, quantity):
        symbol = Wallet.get_symbol(from_currency, to_currency)
        return self.client.create_order(symbol=symbol, side="SELL", type=type_market, quantity=quantity)

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

    def relevant_account_info(self):
        info = self.client.get_account()['balances']
        relevant_info = []
        for row in info:
            if float(row['free']) > 0:
                relevant_info.append(row)
        return relevant_info

    def all_in(self, currency):
        info = self.relevant_account_info()
        if not self.is_valid_for_transfer(currency):
            return False # add to log
        for data in info:
            origin_currency = data['asset']
            dest_currency = "USDT"
            free_quantity = float(data['free'])
            min_qty, step_size = self.min_qty_step_size(origin_currency)
            if min_qty is None or step_size is None:
                continue
            optimal_quantity = round((free_quantity // min_qty) * step_size, 8)
            if self.convertor.from_to(origin_currency, dest_currency) and self.is_valid_lot_size(optimal_quantity, min_qty):
                self.sell(origin_currency, dest_currency, "MARKET", float(optimal_quantity))
            #else:
            #    print(origin_currency)

    def is_valid_for_transfer(self, from_currency):
        return self.convertor.from_to(from_currency, "USDT")

    def is_valid_lot_size(self, optimal_quantity, min_qty): # (quantity-minQty) % stepSize == 0
        return min_qty <= optimal_quantity

    def min_qty_step_size(self, currency):
        symbol_info = self.client.get_symbol_info(Wallet.get_symbol(currency, "USDT"))
        if symbol_info is None:
            return None, None
        return float(symbol_info['filters'][2]['minQty']), float(symbol_info['filters'][2]['stepSize'])

    def get_all_prices(self):
        return self.client.get_all_tickers()


