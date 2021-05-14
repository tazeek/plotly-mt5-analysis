from ForexAnalyzer import ForexAnalyzer

# Fetch the required Forex pairs
forex_pairs = []

with open('forex_pairs.txt') as f:
    for line in f.readlines():
        forex_pairs.append(line.strip())

print(forex_pairs)