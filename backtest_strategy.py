import numpy as np 
import pandas as pd
from datetime import datetime, date
from functools import partial
import math

from backtest_engine import backtest_engine


def consecur_comp(ls, larger=True):
    if len(ls) == 1:
        return True
    if larger:
        return ls[0] > ls[1] and consecur_comp(ls[1:], larger=larger)
    else:
        return ls[0] < ls[1] and consecur_comp(ls[1:], larger=larger)

consevur_comp_gt = partial(consecur_comp, larger=True)
consevur_comp_lt = partial(consecur_comp, larger=False)

def ma(sr: pd.Series):
    windows = [1, 5, 10, 20]
    ma = [ sr[-x:].mean() for x in windows] 
    return [ (ma[0]>max(ma[1:])), -1*(ma[0]<min(ma[1:]))]

def momentum(sr: pd.Series):
    windows = [1, 5, 10, 20]
    mom = [ sr[-x:].mean() for x in windows] 
    return mom

def log_return(sr: pd.Series):
    return (sr/sr.shift(1)).apply(math.log)


# ------------ Momentum strategy - long-short --------------
class backtest_strategy(backtest_engine):
    def strategy(self, data):
        # mind to deal with NaN value, the engine only stream in what is provided, not preprocessing
        position = pd.Series(index=self.symbols)
        price = data.loc[:, (slice(None), 'last')].dropna(how='any', axis='columns')
        price_return = price.dropna(how='any', axis='columns').apply(log_return, axis=0)

        position_ma = price_return.apply(momentum, axis=0, result_type='expand').mean(axis=0).reset_index(level=1, drop=True)
        position_ma = position_ma.sort_values()

        position.loc[position_ma.iloc[0:10]] = 1
        position.loc[position_ma.iloc[-10:]] = -1
        position = position.fillna(0)

        target_position = position[self.symbols].values
        return target_position


""" 
# ------------Move average strategy - long-short --------------
class backtest_strategy(backtest_engine):
    def strategy(self, data):
        # mind to deal with NaN value, the engine only stream in what is provided, not preprocessing
        position = pd.Series(index=self.symbols)
        price = data.loc[:, (slice(None), 'last')].dropna(how='any', axis='columns')

        position_ma = price.apply(ma, axis=0, result_type='expand').sum(axis=0).reset_index(level=1, drop=True)

        position.loc[position_ma.index] = position_ma.values
        position = position.fillna(0)

        target_position = position[self.symbols].values
        return target_position
 """

""" 
# ------------Move average strategy - long --------------
class backtest_strategy(backtest_engine):
    def strategy(self, data):
        # mind to deal with NaN value, the engine only stream in what is provided, not preprocessing
        position = pd.Series(index=self.symbols)
        price = data.loc[:, (slice(None), 'last')].dropna(how='any', axis='columns')

        position_ma = price.apply(ma, axis=0, result_type='expand').iloc[0].reset_index(level=1, drop=True)

        position.loc[position_ma.index] = position_ma.values
        position = position.fillna(0)

        target_position = position[self.symbols].values
        return target_position

 """
""" 
# ---------------- simple open position --------------
class backtest_strategy(backtest_engine):
    def strategy(self, data):
        # mind to deal with NaN value, the engine only stream in what is provided, not preprocessing
        value = data.iloc[-1].loc[(slice(None), 'last')].apply(lambda x: int(~np.isnan(x)))

        target_position = value[self.symbols].values
        return target_position

 """