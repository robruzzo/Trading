# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 20:05:37 2020

@author: robru
"""
portfolio_directory='E:/Portfolios/' #Include the trailing '/'
portfolio_name='mythree/'
data_subdirectory='data/'
ticker_sub_directory ='mythree/'
output_directory='output/'
report_root='reports/'
report_data_directory='data/'

portfolio_root=portfolio_directory+portfolio_name
portfolio_data=portfolio_root+data_subdirectory
portfolio_ticker=portfolio_data+ticker_sub_directory
portfolio_output=portfolio_root+output_directory
report_directory=portfolio_root+report_root
report_data_root=report_directory+report_data_directory

ticker_file='mythree.csv'
output_file='mythree_portfolio.csv'
reference_file='index.pickle'
period="1y"
delay=0.5

import tickerdatautil as td
import pandas as pd

#df = pd.DataFrame(data=['AAPL','IBM','OLED'], columns=['Ticker']) 
#td.convert_tickers_df_to_csv(portfolio_data,ticker_file,df)
td.get_data_from_yahoo(portfolio_directory+portfolio_name+data_subdirectory,ticker_sub_directory,ticker_file,period,False,True,delay)