from ForexAnalyzer import ForexAnalyzer
 
eurgbp_analyzer = ForexAnalyzer('EURGBP')

today_rates = eurgbp_analyzer.get_daily_stats('Minute_1')

print(today_rates)