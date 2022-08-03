import json
from datetime import datetime
from CryptoUtil.DataUtil import DataUtil


class TestWallet:
    def __init__(self, data_util):
        self.data_util = data_util
        self.coin_dict = {"BTC": 0.2, "LTC": 3, "USDT": 1000}

    def invest_on_currency(self, coin, percent):
        for from_coin in self.coin_dict.keys():
            self.convert(from_coin, coin, percent)
        self.report()

    def convert(self, from_, to_, percent):
        self.coin_dict.update(
            {to_: self.coin_dict[to_] + self.coin_dict[from_] * percent * self.data_util.currency_price(from_) / self.data_util.currency_price(to_)})
        # self.coin_dict[from_] += self.coin_dict[to_] * percent
        self.coin_dict.update({from_: self.coin_dict[from_] - self.coin_dict[from_] * percent})
        self.report()

        # self.coin_dict[to_] -= self.coin_dict[to_] * percent

    def report(self):
        print("#########################")
        sum = 0
        for coin in self.coin_dict.keys():
            sum += self.coin_dict[coin] * self.data_util.currency_price(coin)
            print(f"coin {coin} with value of {self.coin_dict[coin]}")
        print(f"total sum is: {sum}")
        print("#########################")