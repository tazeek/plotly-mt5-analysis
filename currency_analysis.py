from src.ForexAnalyzer import ForexAnalyzer

def load_forex_pairs():
    """Load all the symbols
        Source: https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolsget_py

        Parameters:
           None
        
        Returns:
            - list: return all the symbols from the text file
        
    """

    forex_analyzer = ForexAnalyzer.get_instance()

    symbols_list = forex_analyzer.get_symbol_list()
    
    return sorted(symbols_list)

def calculate_currency_strength():

    """Find the currency strength, based on the given symbols

        Parameters:
           None
        
        Returns:
            - dict: return the strength of all currencies, in sorted order (strongest to weakest)
        
    """

    forex_analyzer = ForexAnalyzer.get_instance()
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