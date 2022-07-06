from threading import Thread


class CoinsManager:
    def __init__(self):
        self.indicicators = []
        self.current_threads = []

    def indicator_activate(self, indicator, args):
        # scan a json file that says which indicators to activate and turn them on.
        indicator.execute(args)

    def update_price_prediction(self, symbol):
        # collet the price from all the indicators about a specific coin
        # calculate the predicted price considering the accuracy of each indicator
        pass

    def clean_useless_indicators(self):
        # run through all of the indicators and if there is an indicators with low accuracy on all coins disable it.
        pass

    def append_indicator(self, indicator):
        self.indicicators.append(indicator)

    def recv_indicator_result(self, indicator):
        return indicator.get_results()
