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

## Strategy

**NOTE**: This is only based on a personal opinion after trading, understanding, learning, and researching on how market prices work in general. DO NOT take it as a **get-rich quick idea**. Do try to read on how other traders trade or how their approaches are.

Inspiration from [Rayner Teo's MAEE](https://www.tradingwithrayner.com/the-maee-formula/) and [The Moving Average](https://www.youtube.com/c/TheMovingAverage):

- **M**arket (4H): Observe the market chart. The result is either *trending* or *ranging*.
- **A**rea (4H or 1H): Check if the price is on an area of value (Moving Average, Static/Resistance).
- **E**ntry (1H, 1H or 15M): Check if there are any reasons to enter the market (Candlestick patterns, price rejection, etc). In addition, **observe** the full picture of the trend and decide what needs to be done.
- **E**xit (4H or 1H): Identify the area where you will exit the market from.

Additional Information:

- When observing the market, highlight temporary key areas. Remove them by the end of the day and plot again the next day.
- When looking for an entry point, ***be flexible***. Always be able to trade in more than one way.
- **Exit** when you are wrong. That is when your entire trade set up becomes invalid. Set up your stop-loss at this area.
- **Adjust** your stop-loss every time you cross a profit level. For example: if you cross 100 points of profit, adjust your stop-loss to that level. It is better to **lock your profits and exit** than to **hope** that the price continues going in the intended direction.
- The **ideal** entry position is when the stop-loss is not too far away. Worst-case scenario: a wider-stop loss and the market reverses completely.
- **RECOMMENDED**: Do not keep re-adjusting your stop-loss. If it is invalid, walk away.
- **RECOMMENDED**: Have patience. Let the price come to the area of value. Never enter a trade unknowingly
- **Scalping**: Going against the trend (ex. Retracing) when the price has not reached the area of value. Good for quick profits but highly risky.
- RSI does not work well when the market is in consolidation

References:

If you wish to learn about forex trading, I highly recommend the following:

- Rayner Teo
- The Moving Average
- Babypips
- Reading book