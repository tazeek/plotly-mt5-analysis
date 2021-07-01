from src.ForexAnalyzer import ForexAnalyzer

# Get the stats of each forex pair and store in dictionary
def fetch_latest_candlesticks():

    forex_analyzer = ForexAnalyzer()
    forex_pairs = []

    with open('files\\forex_pairs.txt') as f:
        for line in f.readlines():
            forex_pairs.append(line.rstrip())
            
    candlesticks_width_dict = {}

    for pair in forex_pairs:
        
        forex_analyzer.update_forex_pair(pair)

        pair_stats = forex_analyzer.get_d1_stats()
        candlesticks_width_dict[pair] = pair_stats['width_candlestick']

    # Sort out dictionary in descending order
    candlesticks_width_dict = dict(
        sorted(candlesticks_width_dict.items(), key=lambda item: item[1], reverse=True)
    )

    candlesticks_width_dict['last_updated'] = forex_analyzer.get_current_time(0).strftime("%Y/%m/%d %H:%M:%S")

    # Write to new text file
    with open('files\\candlesticks_width.txt', 'w+') as f:
        for key, value in candlesticks_width_dict.items():
            f.writelines(f"{key}: {value}\n")

    return candlesticks_width_dict

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

    print(currency_strength)

    currency_strength['last_updated'] = forex_analyzer.get_current_time(0).strftime("%Y/%m/%d %H:%M:%S")

    # Write to new text file
    with open('files\\currency_strength.txt', 'w+') as f:
        for key, value in currency_strength.items():
            f.writelines(f"{key}: {value}\n")

    return currency_strength