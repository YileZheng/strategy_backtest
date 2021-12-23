import numpy as np
import pandas as pd
from datetime import datetime, date


data_pool = pd.read_csv("data.csv", index_col='date', parse_dates=True).pivot(columns='ticker')
data_pool = data_pool.swaplevel(1,0, axis=1)

# backtest config
global WINDOW 
global SYMBOLS 
global DATE_START
global DATE_END 

WINDOW = 14
SYMBOLS = data_pool.columns.get_level_values(0).unique()
DATE_START = datetime(2013,1,8)
DATE_END = datetime(2020,1,8)

INIT_CAPITAL = 1000000

assert WINDOW >0

class backtest_engine():
    def __init__(self, data_pool):
        
        self.data_player_gen = self.data_player(data_pool)
        self.init_cap = INIT_CAPITAL

        self.cash = INIT_CAPITAL
        self.market_value = 0

        self.pnl = pd.DataFrame({'date':[], 'pnl':[]})
        self.net_value = pd.DataFrame({'date':[], 'net_value':[]})
        self.cur_pos = None
        self.pos_his = pd.DataFrame(columns=['date'] + SYMBOLS)

    def data_player(self, data_pool: pd.DataFrame):
        data_pool = data_pool[data_pool.index.to_series().between(DATE_START, DATE_END)]
        data_pool = data_pool.sort_index(axis=1, level=0)
        calendar = data_pool.index
        duration = WINDOW+1
        # print(data_pool)
        for i in range(duration-1, len(calendar)):
            data_out = data_pool.iloc[i-duration+1:i,:].loc[:, (SYMBOLS, slice(None))]
            yield data_out
    

    def portfolio_manager(self, target_position, dt, price):
        assert len(target_position)==len(SYMBOLS)

        prc = price[SYMBOLS].values
        open_pos = target_position*prc
        
        self.net_value = self.cash + self.cur_pos*prc
        self.market_value = open_pos
        self.cash = self.net_value - self.market_value
        self.cur_pos = target_position


        self.pnl = self.pnl.append({'date':dt, 'value':open_pos}, ignore_index=True)
        self.pos_his = self.pos_his.append(dict(zip(['date']+SYMBOLS, [dt]+target_position)), ignore_index=True)
        print(f"date {dt}, cash:{}, pnl: {}, postion: {target_position}")

    def strategy(self, data):
        target_position = [1]* len(SYMBOLS)
        return target_position
    
    def end_backtest(self):
        self.pnl.to_csv('pnl.csv', index=False)
        self.pos_his.to_csv('position.csv', index=False)

    def trading_engine(self):
        for backtest_data in self.data_player_gen:
            tod_price = backtest_data.iloc[-1].loc[(SYMBOLS, 'last')]
            today_dt = backtest_data.iloc[-1].index
            his_data = backtest_data.iloc[:-1]
            target_position = self.strategy(his_data)
            self.portfolio_manager(target_position, today_dt, tod_price)

        self.end_backtest()