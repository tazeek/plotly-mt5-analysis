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

## Strategies 