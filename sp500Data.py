# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 22:18:41 2020

@author: Robert E. Ruzzo III

The object of this script is to perform the following tasks:
1. Grab the current List of S&P 500 Company Tickers
2. Using the Yahoo Finance API, Download all the data for a given time period
   and save them to a csv. (open, high, low, close,volume, dividends, stock splits)
3. Update the data when called. In this case the update period will be calculated.
   If the data has not been updated in greater than 3 months, the data should be 
   refreshed using the original grab function, as opposed to the update function.
4. Using any pickle list of stock tickers, download or update the data accordingly.

5. Read a CSV with stock tickers and import them into a pickle file for use as above.
"""


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



'''
Yahoo Finance acceptable time periods:
valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
'''
period ="1y"
daily_period="1d"
delay=0.5

def save_sp_500_tickers():
    resp=requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup =bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table',{'class': 'wikitable sortable'})
    tickers=[]
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace('.','-')
        ticker = ticker[:-1]
        tickers.append(ticker)
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)          #:5 is for testing First 5

    return tickers

#TODO: UPDATE to accept any pickle file with tickers.

def update_ticker_prices_fromLast(ticker):
    with open("sp500tickers.pickle","rb") as f:
            tickers=pickle.load(f)
    for ticker in tickers:
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
                f.write(df.to_csv(header=False,index=False))
                time.sleep(delay)
    
'''
TODO: get_data_from_yahoo:

1. allow for any ticker list to be used that is a pickle
2. allow for the period to be a variable input, but make the default 1 year
3. put a refresh flag, this will delete the old files, re-download and rewrite
4. add directory variable and file name for user input
'''   
def get_data_from_yahoo(reload_sp500):
    if reload_sp500:
        tickers= save_sp_500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers=pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
        
    for ticker in tickers:
        print("Getting Ticker: {}".format(ticker))
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            tick=yf.Ticker(ticker)
            df=tick.history(period)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
            time.sleep(delay)
        else:
            print('Already have {}'.format(ticker))

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

#TODO: Create a file to create or update a pickle file from a CSV list of tickers
