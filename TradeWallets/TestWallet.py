import json
from datetime import datetime
from CryptoUtil.DataUtil import DataUtil


class TestWallet:
    def __init__(self, data_util):
        self.data_util = data_util
        self.coin_dict = {"BTC": 0.0, "LTC": 0, "USDT": 1000}
        self.general_coin = "USDT"

    def convert(self, from_, to_, percent):
        self.coin_dict.update(
            {to_: self.coin_dict[to_] + self.coin_dict[from_] * percent * self.data_util.currency_price(
                from_) / self.data_util.currency_price(to_)})
        self.coin_dict.update({from_: self.coin_dict[from_] - self.coin_dict[from_] * percent})

    def report(self):
        print("________________________")
        sum = 0
        for coin in self.coin_dict.keys():
            sum += self.coin_dict[coin] * self.data_util.currency_price(coin)
            print(f"coin {coin} with value of {self.coin_dict[coin]}")
        print(f"total sum is: {sum}")
        print("________________________")

    def buy(self, coin, percent):
        self.convert(self.general_coin, coin, percent)

    def sell(self, coin, percent):
        self.convert(coin, self.general_coin, percent)
