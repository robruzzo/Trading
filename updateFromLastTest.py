import bs4 as bs
import pickle
import requests
import os
import numpy as np
import time
import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import date


update_period = "1mo"
ticker = "AAPL"
delay =0.5

def update_ticker_prices_fromLast(ticker):
    print("Updating Ticker: {}".format(ticker))
    if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
        print("Ticker File Not Found, Run get_data_from_yahoo()")
    else:
        delta, last_date=get_update_date_delta('{}'.format(ticker))
        if delta==0:
            print("No Update Needed... Exiting")
            exit()
        if delta==1:
            update_period = "1d"
        if delta > 1 and delta < 32:
            update_period ="1mo"
        if delta > 31 and delta < 94:
            update_period ="3mo"
        if delta > 93: 
            print("It has been more than 3 Months since update, it would be more efficient to get new data. \nUse get_data_from_yahoo") 
            print("\nDays Since Last Update: {}  ".format(delta)) 
            exit()
        prior_data=pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        print(prior_data.tail(delta))
        with open('stock_dfs/{}.csv'.format(ticker),"ab") as f:
            tick=yf.Ticker(ticker)
            df=tick.history(update_period)
            df.reset_index(inplace=True)
            #Depedent on Update Time, Get aftermarket volume info
            if update_period =="1d":
                df.drop(df.index[1], inplace=True)
            else:
                row=df.loc[df["Date"] == str(last_date.astype(str).tolist()[0])]
                index = row.index[0]+1
                df=df[index:]
                print(df)   
            f.write(df.to_csv(header=False,index=False))
            time.sleep(delay)
            

def get_update_date_delta(ticker):
    if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            print("Ticker File Not Found, Run get_data_from_yahoo()")
    else:   
            today=datetime.now()
            df=pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df["Date"]=pd.to_datetime(df["Date"])
            last_date=df.tail(1)["Date"]
            difference = today - last_date
            return int(difference.astype('timedelta64[D]')), last_date
            
def print_file_tail(ticker):
    prior_data=pd.read_csv('stock_dfs/{}.csv'.format(ticker))
    print(prior_data.tail(20))


update_ticker_prices_fromLast(ticker)
print_file_tail(ticker)