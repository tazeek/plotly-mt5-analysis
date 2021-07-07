from src.ForexAnalyzer import ForexAnalyzer

def calculate_currency_strength():

    forex_analyzer = ForexAnalyzer()
    forex_pairs = []

    with open('files\\currency_strength_pairs.txt') as f:
        for line in f.readlines():
            forex_pairs.append(line.rstrip())
    
    currency_strength = {
        'JPY': 0.00
    }

    for pair in forex_pairs:
        strength = forex_analyzer.get_currency_strength(pair)

        currency_strength[pair[:3]] = strength

    # Sort out dictionary in descending order
    currency_strength = dict(
        sorted(currency_strength.items(), key=lambda item: item[1], reverse=True)
    )

    return currency_strength