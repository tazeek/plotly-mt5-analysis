import math

class RiskManager:

    def calculate_remaining_trades(self, para_dict):

        amount = para_dict['current_balance'] - para_dict['buffer_balance']
        risk_vol = para_dict['pip_loss'] * para_dict['leverage']

        return math.ceil(amount / risk_vol)


    def calculate_pips_profit(self, para_dict):

        profit_aim = para_dict['profit']
        min_trades = para_dict['min_trades_profit']
        leverage = para_dict['leverage']

        return math.ceil(profit_aim / (min_trades * leverage))