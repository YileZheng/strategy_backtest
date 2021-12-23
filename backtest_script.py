import numpy as np 
import pandas as pd
from datetime import datetime, date

from backtest_engine import backtest_engine, data_pool
from backtest_strategy import backtest_strategy

bktst = backtest_strategy(data_pool)
bktst.trading_engine()