from src.ForexAnalyzer import ForexAnalyzer

# Get the stats of each forex pair and store in dictionary
def fetch_latest_candlesticks(forex_pairs):

    forex_analyzer = ForexAnalyzer()
    
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