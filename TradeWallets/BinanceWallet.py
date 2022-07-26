import logging

from binance.client import Client
import pandas as pd


class BinanceWallet:
    def __init__(self, api_key, api_secret, risk, wallet_name, config):
        self.api_key, self.api_secret = BinanceWallet.making_api_key(api_key, api_secret)
        self.client = self.connect()
        self.risk = risk  # number between 0 -> 1
        self.wallet_name = wallet_name
        self.config_file = config
        self.init_logger(wallet_name, config)

    def init_logger(self, logger_name, config_file):
        # Create a custom logger
        logger_path = config_file["Paths"]["abs_path"] + config_file["Paths"]["logger_folder"] + config_file["Paths"][
            "trade_wallet_logs_path"]
        logger_full_path = logger_path + logger_name + ".log"
        self.logger = logging.getLogger(name=logger_name)
        log_formatter = logging.Formatter(config_file["Logger"]["wallet_log_format"])
        log_file_handler = logging.FileHandler(
            logger_full_path, mode=config_file["Logger"]["wallet_log_filemode"]
        )
        log_file_handler.setFormatter(log_formatter)
        self.logger.addHandler(log_file_handler)
        self.logger.setLevel(config_file["Logger"]["wallet_log_setting_level"])
        self.logger.info("Initialize logger")

    def convert(self, first_coin, second_coin, percent, type_market="MARKET"):
        if first_coin == "USDT":
            return False
        # I want to convert % of my FirstCoin to the SecondCoin
        if first_coin == second_coin:
            self.logger.warning(f"Trying to convert from {first_coin} to {second_coin}")
            return False
        self.logger.info(f"Start to convert from {first_coin} to {second_coin} with Percent : {percent}")
        try:
            self.direct_convert(second_coin, first_coin, percent, "BUY",
                                type_market)  # "BTCLTC" i want to buy BTC using LTC
        except Exception as e1:
            try:
                self.logger.warning(f"Failed to convert with first opportunity, {e1}")
                self.direct_convert(first_coin, second_coin, percent, "SELL", type_market)
            except Exception as e2:
                self.logger.warning(f"Failed to convert with second opportunity, {e2}")
                try:
                    self.direct_convert(first_coin, "BUSD", percent, "SELL", type_market)
                    self.direct_convert(second_coin, "BUSD", 1, "BUY", type_market)
                except Exception as e3:
                    self.logger.error(f"Failed to convert, {e3}")
                    return False
        self.logger.info(f"Successfully converted from {first_coin} to {second_coin}")
        return True

    def get_quan_to_trade(self, first_coin, second_coin, percent, side):
        first_coin_balance = self.get_currency_balance(first_coin)
        second_coin_balance = self.get_currency_balance(second_coin)
        if side == "BUY":
            return round(self.get_two_currency_rate(second_coin, first_coin) * second_coin_balance * percent, 8)
        elif side == "SELL":
            return round(first_coin_balance * percent, 8)
        else:
            return 0

    def direct_convert(self, first_coin, second_coin, percent, side, type_market):
        quantity = self.get_quan_to_trade(first_coin, second_coin, percent, side)
        symbol = BinanceWallet.get_symbol(first_coin, second_coin)
        self.logger.info(f"Quantity : {quantity} for Symbol : {symbol}")
        min_qty, step_size = self.min_qty_step_size(first_coin)
        if min_qty is None or step_size is None:
            return 0
        optimal_quantity = round((quantity // min_qty) * step_size, 8)
        if self.is_valid_lot_size(optimal_quantity, min_qty):
            self.client.create_order(symbol=symbol, side=side, type=type_market, quantity=optimal_quantity)
        return optimal_quantity

    def currency_price(self, currency):
        if currency == "USDT":
            return 1
        df = pd.DataFrame(self.client.get_all_tickers())
        df = df[df['symbol'] == BinanceWallet.get_symbol(currency, "BUSD")]
        return float(df['price'].iloc[0])

    def connect(self):
        return Client(self.api_key, self.api_secret)

    @staticmethod
    def get_symbol(from_currency, to_currency):
        return from_currency + to_currency

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

    def invest_on_currency(self, currency, percent):  # percent 0->1
        df = self.relevant_account_info()
        for data in df.iterrows():
            self.convert(data[1]['asset'], currency, percent, "MARKET")
        return

    def is_valid_lot_size(self, optimal_quantity, min_qty):  # (quantity-minQty) % stepSize == 0
        return min_qty <= optimal_quantity

    def min_qty_step_size(self, currency):
        symbol_info = self.client.get_symbol_info(BinanceWallet.get_symbol(currency, "BUSD"))
        if symbol_info is None:
            return None, None
        return float(symbol_info['filters'][2]['minQty']), float(symbol_info['filters'][2]['stepSize'])

    def get_all_prices(self):
        return self.client.get_all_tickers()

    def get_currency_balance(self, currency):
        return float(self.client.get_asset_balance(asset=currency)['free'])

    def making_api_key(api_key, api_secret):
        return api_key, api_secret

    def get_two_currency_rate(self, first_coin, second_coin):
        first_coin_price = self.currency_price(first_coin)
        second_coin_price = self.currency_price(second_coin)
        return first_coin_price / second_coin_price

    def aggregate_trade(self, first_coin, second_coin, min_ago):
        try:
            symbol = self.get_symbol(first_coin, second_coin)
            agg_trades = self.client.aggregate_trade_iter(symbol=symbol, start_str=str(min_ago) + ' minutes ago UTC')
            return agg_trades
        except Exception:
            return False

    def get_tickers(self):
        tickers = self.client.get_orderbook_tickers()
        return tickers

    def get_depth(self, first_coin, second_coin):
        try:
            symbol = self.get_symbol(first_coin, second_coin)
            depth = self.client.get_order_book(symbol=symbol)
            return depth
        except Exception:
            return False

    # @staticmethod
    # def create_new_logger(logger_name, config_file, log_path):
    #     # Create a custom logger
    #     logger_path = config_file["Paths"]["abs_path"] + config_file["Paths"]["logger_folder"] + config_file["Paths"][
    #         "trade_wallet_logs_path"]
    #     logger_full_path = logger_path + logger_name + ".log"
    #     # Creating and Configuring Logger
    #     Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    #     print(logger_full_path)
    #     logging.basicConfig(filename=logger_full_path,
    #                         filemode="a",
    #                         format=Log_Format,
    #                         level=logging.INFO)
    #     # logger = logging.getLogger()
    #     return logger_full_path

