import numpy as np 
import pandas as pd
from datetime import datetime, date

from backtest_engine import backtest_engine, data_pool


bktst = backtest_engine(data_pool)
bktst.trading_engine()