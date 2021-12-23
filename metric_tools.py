import numpy as np 
import pandas as pd

def strategy_performance_metrics(sr_return: pd.Series, freq='D', options='h'):
	# input: 
	# sr_return: series of return, which is usually between [1,-1], time ascend series
	# freq: the period of the return, D: daily, M: monthly, W: weekly, Y: annually
	# options: string contains option charactors like bash
	# - h: for human reading, transfer all numerical output to strings and into percentage if appliable
	# output:
	# Series with metrics names as index
	# author: Leon Zheng
	
	# pre parameters parse
	freq_to_annual = {
		'D':252,
		'W':52,
		'M':12,
		'Y':1
	}
	readable = 'h' in options
	period = freq_to_annual[freq]
	nan_ind = sr_return[sr_return.isnull()].index.tolist()
	
	print("calculate annual metrics by freq: ", freq)
	if len(nan_ind):
		print("Contain NaNs!!!")
		print("Drop row in index: ", nan_ind)
	
	# functions
	def get_max_drawdown(net_value: pd.Series):
		ind_max_draw = np.argmax(np.maximum.accumulate(net_value) - net_value)
		ind_max_before = np.argmax(net_value[:ind_max_draw])
		max_dd = (net_value[ind_max_draw] - net_value[ind_max_before]) / net_value[ind_max_before]
		return -max_dd
	
	# indicators for use
	r = sr_return.dropna().copy()          # oscilating around 0
	net_value = (r+1).cumprod()   # start from 1
	pnl = net_value-1             # start from 0
	
	return_mean = r.mean()
	return_p_a = return_mean*period
	return_cum = pnl.iloc[-1]
	std_p_a = r.std()*np.sqrt(period)
	max_drawdown = get_max_drawdown(net_value)
	sharpe_ratio = return_p_a/std_p_a           #TODO  -risk free ?
	calmar_ratio = return_p_a/max_drawdown      #TODO 36 month?
	win_rate = (r>0).sum()/len(r)               #TODO transaction?
	
	# write into the table
	metrics_names = ['Sharpe Ratio','Calmar Ratio','Win Rate','Max Drawdown',
					 'Cumulate Return Ratio','Return p.a.','Std p.a.']
	sr_metrics = pd.Series(index=metrics_names)
	sr_metrics['Sharpe Ratio'] = f"{sharpe_ratio:.4f}" if readable else sharpe_ratio
	sr_metrics['Calmar Ratio'] = f"{calmar_ratio:.4f}" if readable else calmar_ratio
	sr_metrics['Win Rate'] =    f"{win_rate*100:.4f}%" if readable else win_rate  
	sr_metrics['Max Drawdown'] = f"{max_drawdown*100:.4f}%" if readable else  max_drawdown
	sr_metrics['Cumulate Return Ratio'] = f"{return_cum*100:.4f}%" if readable else return_cum
	sr_metrics['Return p.a.'] = f"{return_p_a*100:.4f}%" if readable else return_p_a
	sr_metrics['Std p.a.'] =    f"{std_p_a*100:.4f}%" if readable else std_p_a
	
	return sr_metrics
