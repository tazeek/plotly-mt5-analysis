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

    """Find the currency strength, based on JPY pairs

        Parameters:
           None
        
        Returns:
            - dict: return the strength of all currencies, in sorted order (strongest to weakest)
        
    """

    forex_analyzer = ForexAnalyzer.get_instance()

    return forex_analyzer.get_currency_strength()