from binance.client import Client


class Wallet:
    def __init__(self, api_key, api_secret):
        self.api_key, self.api_secret = Wallet.making_api_key(api_key, api_secret)
        self.client = self.connect()

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