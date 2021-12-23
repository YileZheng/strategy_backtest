# strategy_backtest
> _by Leon Zheng_

This work contains 3 aspects:
1. Backtest engine design: in file _backtest_engine.py_ \
   It consists of a data player, a portfolio manager and a core strategy 
2. Strategy development: in file _backtest_strategy.py_
3. Backtest result analysis: in file _result_analysis.ipynb_

## File description:
.                               
├── README.md                   
├── backtest_engine.py --------------------- # the backtest engine \
├── backtest_script.py ---------------------- # the script to run the backtesting \
├── backtest_strategy.py -------------------- # the strategy \
├── data.csv --------------------------------- # data pool for the backtest \
├── environment.yml ------------------------- # conda environment \
├── net_value.csv --------------------------- # result of the backtest: net value \
├── pnl.csv ---------------------------------- # result of the backtest: profit and lost \
├── position.csv ----------------------------- # result of the backtest: position details \
├── result_analysis.ipynb -------------------- # a Jupyter Notebook to analysis the backtest result \
├── metric_tools.py ------------------------- # utilities for result analysis \
└── result_analysis.ipynb -------------------- # Analysis of the backtest outcome

---------------


## Usage
### __Python environment__

To install the environment, make sure you have conda on your machine, run:
```
conda env create -f environment.yml
```

### __Backtest configuration__

You can change the configuration of the backtest engine at the beginning of the file _backtest_engine.py_ \
The parameters:

| Parameter name | description |
| - | - |
|WINDOW     | The length of the historical data that you want the strategy to see |  |
|SYMBOLS    | Symbols of stocks that you want the strategy to see |  |
|DATE_START | Start day of the backtest peroid |  |
|DATE_END   | End day of the backtest peroid |  | 
|INIT_CAPITAL| Initial capital


### __Strategy__

One can write his/her own strategy inside the backtest_strategy class in file _backtest_strategy.py_ 

I have already developed 4 different strategies in the file:
1. __Long-short momentum strategy:__ calculate the mean of log returns in time windows with different lengths, then average them to get the momentum of one stock. Sort by their value. Long top 10, and hedge by short last 10.
2. __Long-only moving average strategy:__ calculate the mean of log returns in time windows with different lengths. If the current price is greater than all of the averages, long.
3. __Long-short moving average strategy:__ similar with the last one, but hedge by short ones whose current price is less then all of the averages.
4. __Long whatever available:__ very simple and naive strategy, long everything that has a price.


### __Resume the backtest engine__
To run the backtest engine, please directly run:

``` 
python backtest_script.py
```

After finishing the running, there will be 3 .csv files in the root directory (i.e. net_value.csv, pnl.csv, position.csv), which indicate the portfolio details in every day.

### __Analyze results__

The utility in the file _metric_tool.py_ can be used to analyse several metrics of the net value outcomes. It can also be used to analyse several return curves by applying it to a DateFrame of a number of return sequences. \ 

The file _result_analysis.ipynb_ shows plots of the net value and PNL (profit and lost) and strategy performance metrics including Sharpe ratio, max drawdown, return rate and etc of the aforementioned strategies. \

