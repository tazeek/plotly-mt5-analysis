from ForexAnalyzer import ForexAnalyzer

# Fetch the required Forex pairs
forex_pairs = []

with open('forex_pairs.txt') as f:
    for line in f.readlines():
        forex_pairs.append(line.strip())

forex_analyzer = ForexAnalyzer()

# Get the stats of each forex pair and store in dictionary
candlesticks_width_dict = {}

for pair in forex_pairs:
    
    forex_analyzer.update_forex_pair(pair)

    pair_stats = forex_analyzer.get_d1_stats()
    candlesticks_width_dict[pair] = pair_stats['width_candlestick']

# Sort out dictionary in descending order
candlesticks_width_dict = dict(
    sorted(candlesticks_width_dict.items(), key=lambda item: item[1], reverse=True)
)

# Write to new text file
with open('candlesticks_width.txt', 'w+') as f:
    for key, value in candlesticks_width_dict.items():
        f.writelines(f"{key}: {value}\n")