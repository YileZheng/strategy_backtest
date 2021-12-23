# strategy_backtest

Please ignore the ipynb file for now, it is for my own early stage debugging. 

To run the backtest engine, please directly run:

``` bash
python backtest_script.py
```

You can change the configuration of the backtest engine at the beginning of the file _backtest_engine.py_
The parameters:
| Parameter name | description |
| - | - |
|WINDOW     | The length of the historical data that you want the strategy to see |  |
|SYMBOLS    | Symbols of stocks that you want the strategy to see |  |
|DATE_START | Start day of the backtest peroid |  |
|DATE_END   | End day of the backtest peroid |  | 
|INIT_CAPITAL| Initial capital