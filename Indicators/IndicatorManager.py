from threading import Thread


class IndicatorManager:

    def indicators_activate(self):
        # scan a json file that says which indicators to activate and turn them on.
        pass

    def update_price_prediction(self, symbol):
        # collet the price from all the indicators about a specific coin
        # calculate the predicted price considering the accuracy of each indicator
        pass

    def clean_useless_indicators(self):
        # run through all of the indicators and if there is an indicators with low accuracy on all coins disable it.
        pass

