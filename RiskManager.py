import math

class RiskManager:

    def calculate_remaining_trades(para_dict):

        amount = para_dict['balance'] - para_dict['buffer']
        risk_vol = para_dict['pip_loss'] - para_dict['leverage']

        return Math.ceil(amount / risk_vol)


    def calculate_pips_profit(para_dict):

        profit_aim = para_dict['profit']
        min_trades = para_dict['min_trades']

        ...