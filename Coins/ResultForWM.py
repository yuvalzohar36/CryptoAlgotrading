class ResultForWM:
    def __init__(self, args):

        self.coin = args[0]
        self.buy_votes_credit = args[1]
        self.sell_votes_credit = args[2]
        self.hold_votes_credit = args[3]
        self.buy_votes_count = args[4]
        self.sell_votes_count = args[5]
        self.hold_votes_count = args[6]
        self.result_creation = args[7]
        self.max_duration = args[8]

    def assessment(self):
        safe_range = 0.9
        if self.sell_votes_credit*safe_range > self.buy_votes_credit:
            return "SELL"

        elif self.sell_votes_credit < self.buy_votes_credit*safe_range:
            return "BUY"
        return "HOLD"




