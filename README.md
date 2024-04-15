# ChesleyAlgo: Robo-Advisor algorithm using seasonality strategy

This algorithm puruses a strategy of following the stock market direction and presents portfolio according to investor's risk tolerance and market condition. The goal of this Robo-advisor algorithm is providing optimal portfolio suitable for investor's propensity while achieving returns exceeding the benchmark S&P500 index.

## Asset allocation 
Based on the investors' risk tolerance level, they can select portfolio model type allocating different asset classes (equity, fixed income, cash). Monthly reblancing occured as a basis.
- Aggresive portfolio: Max of stock allocation is 100%.
- Growth portfolio: Max of stock allocation is 70%, the rest is to fixed income and cash.
- Moderate portfolio: Max of stock allocation is 30%, the rest is to fixed income and cash.
- Conservative portfolio: 100% fixed income and cash asset.

## Backtesting Result
Compared the performance of **aggresive portfolio** consisting entirely of stocks for the last 20 years against S&P500 benchmark, ChesleyAlgo model returned higher return and higher sharpe ratio.
<p align="left">
  <img alt="Dark" src="Images/backtest.png" width="80%"> 
</p>


## Credit
 
- **Eugene Park** <a href="https://github.com/parkakn" target="_blank">Github</a>, <a href="https://www.linkedin.com/in/eugene-park-" target="_blank">Linkedin</a>
