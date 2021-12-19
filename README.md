# plotly-mt5-analysis
---

### About the project

This project is an analysis done on the forex prices from MetaTrader5 (MT5). The analysis is in the form of a dashboard, which have the following features:

* Currency Strength Analysis
* Currency Coorelation
* Risk Management Analysis
* Price action trading
* Support and Resistance
* Relative Strength Index (RSI) Divergences
* Multi-timeframe Analysis

In the trading community, it is recommended that you should have two different charts when viewing the same forex market: one for analysis, one for making your trades. Hence, the need for a second dashboard (which is this project itself! :laughing:).

## Tools Used

The main tools used for this project are:

- MetaTrader5 API: For fetching prices
- Plotly: Data Visualization purposes
- Dash: Dashboard framework
- Others: Other tools for the purpose of technical analysis

## Picking the symbols

1. Observe the **Currency Strength Analysis**
2. Symbols divided into two categories: **Uptrend** or **Downtrend**
3. The strength of the trend is divided into two: **Weak** or **Strong**
4. Based on the symbols, download the weekly activity of the previous week
5. Check if the symbols were actively traded or not

**Hypothesis**: A symbol that is not commonly traded will have a wider spread.

In addition, check the **coorelation of the chosen symbols**. Symbols that are strongly coorelated (either positively or negatively) should be narrowed down as much as possible, or discarded as well.

## Economic Events

Economic events can be downloaded for the current day only. It is divided into:

- **Currency**: The given currency affected
- **Time**: The time at which the economic event takes place
- **Impact**: How big of an impact is the economic event

## Additional Information:

- When observing the market, highlight temporary key areas. Remove them by the end of the day and plot again the next day.
- When looking for an entry point, ***be flexible***. Always be able to trade in more than one way.
- **Exit** when you are wrong. That is when your entire trade set up becomes invalid. Set up your stop-loss at this area.
- **Adjust** your stop-loss every time you cross a profit level. For example: if you cross 100 points of profit, adjust your stop-loss to that level. It is better to **lock your profits and exit** than to **hope** that the price continues going in the intended direction.
- The **ideal** entry position is when the stop-loss is not too far away. Worst-case scenario: a wider-stop loss and the market reverses completely.
- **RECOMMENDED**: Do not keep re-adjusting your stop-loss. If it is invalid, walk away.
- **RECOMMENDED**: Have patience. Let the price come to the area of value. Never enter a trade unknowingly
- **Scalping**: Going against the trend (ex. Retracing) when the price has not reached the area of value. Good for quick profits but highly risky.
- RSI does not work well when the market is in consolidation

## References

If you wish to learn about forex trading and the concepts related to it, I highly recommend the following:

- [Rayner Teo](https://www.tradingwithrayner.com/): Contains a lot of information and examples regarding a lot of information related to pricing and area of value (I learned MAEE from here).

- [The Moving Average](https://www.youtube.com/channel/UCYFQzaZyTUzY-Tiytyv3HhA): Good information and visual explanation on how different concepts of indicators works (I love the re-test explanation here, as well as the importance of patience).

- [Babypips](https://www.babypips.com/): A lot of humerous explanations on the different trading concepts.

- [Technical Analysis Of The Financial Markets](https://cdn.preterhuman.net/texts/unsorted2/Stock%20books%20029/John%20J%20Murphy%20-%20Technical%20Analysis%20Of%20The%20Financial%20Markets.pdf?fbclid=IwAR0CZjfQf2Mj_ObvDlkTbSf-5SS7WTfvu5hZzKtwDcRRO3-co1X386Is_9M): A good book that explains the logic on why the price behaves as it is and detailed information on the indicators.

**NOTE**: These are just the resources that I learned from mainly. There are tons of research, blogs, and videos available on the internet that explains price action as well. Hence, do take it with an open mind :)