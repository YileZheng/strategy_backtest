# strategy_backtest

This work contains 3 aspects:
1. Backtest engine design: in file _backtest_engine.py_
2. Strategy development: in file _backtest_strategy.py_
3. Backtest result analysis: in file _result_analysis.ipynb_

## Usage
To run the backtest engine, please directly run:

``` bash
python backtest_script.py
```

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
└── str_bkt.ipynb ---------------------------- # just for debugging 


## Backtest configuration
You can change the configuration of the backtest engine at the beginning of the file _backtest_engine.py_
The parameters:
| Parameter name | description |
| - | - |
|WINDOW     | The length of the historical data that you want the strategy to see |  |
|SYMBOLS    | Symbols of stocks that you want the strategy to see |  |
|DATE_START | Start day of the backtest peroid |  |
|DATE_END   | End day of the backtest peroid |  | 
|INIT_CAPITAL| Initial capital


## Strategy
You can write your strategy inside the backtest_strategy class. 