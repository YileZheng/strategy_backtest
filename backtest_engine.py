import numpy as np
import pandas as pd
from datetime import datetime, date


data_pool = pd.read_csv("data.csv", index_col='date', parse_dates=True).pivot(columns='ticker')
data_pool = data_pool.swaplevel(1,0, axis=1)

# backtest config

WINDOW = 14
SYMBOLS = data_pool.columns.get_level_values(0).unique().tolist()
DATE_START = datetime(2013,1,8)
DATE_END = datetime(2020,1,8)

INIT_CAPITAL = 1000000

assert WINDOW >0, "window length should be larger than or equal to 1"
assert DATE_END > DATE_START, "Backtest end date should be later than start date"
assert len(SYMBOLS), "please specify at least one symbol name that is in the data pool"

class backtest_engine():
    def __init__(self, data_pool):
        
        self.data_player_gen = self.data_player(data_pool)
        self.symbols = SYMBOLS
        self.init_cap = INIT_CAPITAL

        self.cash = INIT_CAPITAL
        self.market_value = 0
        self.net_value = INIT_CAPITAL
        self.cur_pos = [0] * len(self.symbols)
        self.pnl = 0

        self.pnl_his = pd.DataFrame({'date':[], 'pnl':[]})
        self.net_value_his = pd.DataFrame({'date':[], 'value':[]})
        self.pos_his = pd.DataFrame(columns=['date'] + self.symbols)

    def data_player(self, data_pool: pd.DataFrame):
        data_pool = data_pool[data_pool.index.to_series().between(DATE_START, DATE_END)]
        data_pool = data_pool.sort_index(axis=1, level=0)
        calendar = data_pool.index
        duration = WINDOW+1
        # print(data_pool)
        for i in range(duration, len(calendar)):
            data_out = data_pool.iloc[i-duration:i,:].loc[:, (self.symbols, slice(None))]
            yield data_out
    

    def portfolio_manager(self, target_position, dt, price):
        assert len(target_position)==len(self.symbols)

        prc = price[self.symbols].fillna(0).values
        open_pos = np.dot(target_position, prc)
        self.pnl = self.cash + np.dot(self.cur_pos, prc) - self.net_value
        self.net_value = self.cash + np.dot(self.cur_pos, prc)
        self.market_value = open_pos
        self.cash = self.net_value - self.market_value
        self.cur_pos = target_position

        self.pnl_his = self.pnl_his.append({'date':dt, 'pnl':self.pnl}, ignore_index=True)
        self.pos_his = self.pos_his.append({**{'date': dt}, **dict(zip(self.symbols, self.cur_pos))}, ignore_index=True)
        self.net_value_his = self.net_value_his.append({'date':dt, 'value':self.net_value}, ignore_index=True)
        print(f"Date - {dt.date()}, net_value: {self.net_value}, \tmarket_value: {self.market_value}, \tcash:{self.cash}")

    def strategy(self, data):
        # mind to deal with NaN value, the engine only stream in what is provided, not preprocessing
        position = pd.DataFrame(columns=self.symbols)
        price = data.loc[:, (slice(None), 'last')]
        volume = data.loc[:, (slice(None), 'volume')]

        position = position.fillna(0)
        value = data.iloc[-1].loc[(slice(None), 'last')].apply(lambda x: int(~np.isnan(x)))

        target_position = value[self.symbols].values
        return target_position
    
    def end_backtest(self):
        self.pnl_his.to_csv('pnl.csv', index=False)
        self.pos_his.to_csv('position.csv', index=False)
        self.net_value_his.to_csv('net_value.csv', index=False)

    def trading_engine(self):
        for backtest_data in self.data_player_gen:
            tod_price = backtest_data.iloc[-1].loc[(self.symbols, 'last')]
            today_dt = backtest_data.iloc[-1].name
            his_data = backtest_data.iloc[:-1]
            target_position = self.strategy(his_data)
            self.portfolio_manager(target_position, today_dt, tod_price)

        self.end_backtest()