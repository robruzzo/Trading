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

Notes:

Yahoo Finance acceptable time periods:
valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                Intraday data cannot extend last 60 days
"""

#imports

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
import glob as g

#Global Variables
period ="1y" #Default Initial Yahoo Finance Download Period
delay=0.5	 #Default Delay between downloads in seconds
data_directory='E:/Datasets/Stocks/' #Include the trailing '/'
fileName ="MyWatchList.pickle" #Default File Name For updating
ticker_sub_directory ='test'
start_date='2005-01-01'
end_date='2020-01-01'
interval='1d'


'''
Function Name: save_sp_500_tickers(data_directory)
Function Purpose: To get the current list of S&P500 ticker Symbols from wikipedia
				  and save them to a file tickers.pickle. 
Output: sp500tickers.pickle
'''
def save_sp_500_tickers(data_directory=data_directory):
	resp=requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup=bs.BeautifulSoup(resp.text, 'lxml')
	table=soup.find('table',{'class': 'wikitable sortable'})
	tickers=[]
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text.replace('.','-')
		ticker = ticker[:-1]
		tickers.append(ticker)
	if os.path.exists(data_directory+'sp500tickers.pickle'):
		os.remove(data_directory+'sp500tickers.pickle')
	with open(data_directory + "sp500tickers.pickle","wb") as f:
		pickle.dump(tickers,f)



'''
Function Name: update_ticker_prices_fromLast(data_directory=data_directory,ticker_sub_directory=ticker_sub_directory,fileName=fileName)
Function Purpose: When given a pickle file with a list of ticker names, if a csv file exists in the ticker subdirectory,
				  then the function will check the last date in the file, download the data in a valid increment,
				  and update the file.
'''
def update_ticker_prices_fromLast(data_directory=data_directory,ticker_sub_directory=ticker_sub_directory,fileName=fileName):
	with open(data_directory + fileName,"rb") as f:
			tickers=pickle.load(f)
	for ticker in tickers:
		print("Updating Ticker: {}".format(ticker))
		if not os.path.exists(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker)):
			print("Ticker File Not Found, Check directory, ticker name, or run get_data_from_yahoo()")
		else:
			delta, last_date=get_update_date_delta('{}'.format(ticker))
			if delta==0:
				print("No Update Needed for {}".format(ticker))
				continue
			if delta==1:
				update_period = "1d"
			if delta > 1 and delta < 32:
				update_period ="1mo"
			if delta > 31 and delta < 94:
				update_period ="3mo"
			if delta > 93: 
				print("It has been more than 3 Months since update, it would be more efficient to get new data. \nUse get_data_from_yahoo") 
				print("\nDays Since Last Update: {}  ".format(delta)) 
				continue
			prior_data=pd.read_csv(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker))
			with open(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker),"ab") as f:
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
Function Name: get_data_from_yahoo(data_directory=data_directory,ticker_sub_directory=ticker_sub_directory,fileName=fileName,period=period, refresh=False)
Purpose:  This function will take as an input a pickle file
		  which it will open, take in all of the ticker names
		  and download the information using the Yahoo Finance API.
Arguments:	data_directory: Data parent directory - this is where the pickle files should be stored
			ticker_sub_directory: String, data sub directory, this is where a csv for each of the tickers history will be stored
			fileName: String, file name of the pickle file that resides in the data_directory to read tickers from. The
					  default is sp500tickers.pickle, other pickle files in the same format can be used.
			period: This is the length of the history that you wish to download.
					The following values are allowed for the Yahoo Finance API: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
					The default period is set to 1y or 1 year. The input is a string.
			refresh: Bool, if set to True, it will delete the file for each ticker, and re-download the data for the desired period.
			purge:   Bool, if set to True, ALL data files in the directory will be deleted, and then the data will be downloaded. This
					 function serves to delete old data that is in the directory that is no longer in use. IE after a watch list has changed.
'''
def get_data_from_yahoo(data_directory=data_directory,ticker_sub_directory=ticker_sub_directory,fileName=fileName,period=period,refresh=False, purge=False):
	if not os.path.exists(data_directory+fileName):
		print(data_directory+fileName+" Not Found! Check Path and File Name! Exiting!")
		exit()
	with open(data_directory + fileName,"rb") as f:
		tickers=pickle.load(f)
	if purge:
		files=g.glob(data_directory+ticker_sub_directory+'/*')
		print("Purging all files for a fresh clean start")
		for f in files:
			os.remove(f)
	if not os.path.exists(data_directory+ticker_sub_directory):
		os.makedirs(data_directory+ticker_sub_directory)
	for ticker in tickers:
		if not os.path.exists(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker)):
			print("Getting Ticker: {}".format(ticker))
			tick=yf.Ticker(ticker)
			df=tick.history(period=period)
			df.to_csv(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker))
			time.sleep(delay)
			continue
		if os.path.exists(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker)) and refresh:
			print("Refreshing data for {}".format(ticker))
			os.remove(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker))
			tick=yf.Ticker(ticker)
			df=tick.history(period)
			df.to_csv(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker))
			time.sleep(delay)

'''
Function Name: get_data_from_yahoo_specific(data_directory=data_directory,ticker_sub_directory=ticker_sub_directory,fileName=fileName,period=period, refresh=False)
Purpose:  This function will take as an input a pickle file
		  which it will open, take in all of the ticker names
		  and download the information using the Yahoo Finance API.
Arguments:	data_directory: Data parent directory - this is where the pickle files should be stored
			ticker_sub_directory: String, data sub directory, this is where a csv for each of the tickers history will be stored
			fileName: String, file name of the pickle file that resides in the data_directory to read tickers from. The
					  default is sp500tickers.pickle, other pickle files in the same format can be used.
			start:    A string in the format yyyy-mm-dd representing the desired start date
			end:	  A string in the format yyyy-mm-dd representing the desired end date
			interval: A string representing the interval period for each data point. 
					  Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                      Intraday data cannot extend last 60 days
			refresh:  Bool, if set to True, it will delete the file for each ticker, and re-download the data for the desired period.
			purge:    Bool, if set to True, ALL data files in the directory will be deleted, and then the data will be downloaded. This
					  function serves to delete old data that is in the directory that is no longer in use. IE after a watch list has changed.
'''
def get_data_from_yahoo_specific(data_directory=data_directory,ticker_sub_directory=ticker_sub_directory,fileName=fileName,start=start_date,end=end_date,interval=interval, refresh=False, purge=False):
	if not os.path.exists(data_directory+fileName):
		print(data_directory+fileName+" Not Found! Check Path and File Name! Exiting!")
		exit()
	with open(data_directory + fileName,"rb") as f:
		tickers=pickle.load(f)
	if purge:
		files=g.glob(data_directory+ticker_sub_directory+'/*')
		print("Purging all files for a fresh clean start")
		for f in files:
			os.remove(f)
	if not os.path.exists(data_directory+ticker_sub_directory):
		os.makedirs(data_directory+ticker_sub_directory)
	for ticker in tickers:
		if not os.path.exists(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker)):
			print("Getting Ticker: {}".format(ticker))
			tick=yf.Ticker(ticker)
			df=tick.history(start=start_date,end=end_date,interval=interval)
			df.to_csv(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker))
			time.sleep(delay)
			continue
		if os.path.exists(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker)) and refresh:
			print("Refreshing data for {}".format(ticker))
			os.remove(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker))
			tick=yf.Ticker(ticker)
			df=tick.history(period)
			df.to_csv(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker))
			time.sleep(delay)
'''
Function Name: get_update_delta(ticker)
Purpose: This function takes a ticker name string as an input and will open
		 the appropriate csv file, and will return the time in days since last
		 update as well as the date of the last update.
Returns: int days, pandas datetime last_date yyyy-mm-dd
'''

def get_update_date_delta(ticker):
	if not os.path.exists(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker)):
			print("Ticker File Not Found, Run get_data_from_yahoo()")
	else:   
			today=datetime.now()
			df=pd.read_csv(data_directory+ticker_sub_directory+'/{}.csv'.format(ticker))
			df["Date"]=pd.to_datetime(df["Date"])
			last_date=df.tail(1)["Date"]
			difference = today - last_date
			return int(difference.astype('timedelta64[D]')), last_date


'''
Function Name: convert_tickers_csv_to_pickle(csv_file)
Purpose: This function takes a csv file of one column with ticker names and creates a pickle
		 file with the same name.
'''
def convert_tickers_csv_to_pickle(csv_file):
	df=pd.read_csv(data_directory+csv_file)
	pickle_name=csv_file[:-4]+".pickle"
	tickers=df['Ticker']
	with open(data_directory + pickle_name,"wb") as f:
		pickle.dump(tickers,f)

'''
Function Name: add_ticker_to_pickle(pickleFile,tickerName)
Purpose: This function allows you to add a ticker to a pickle file. Ex myWatchList.
Note: This does not update the data, you should run get_data_from_yahoo() to do so
'''

def add_ticker_to_pickle(pickleFile,tickerName):
	if os.path.exists(data_directory+pickleFile):
		with open(data_directory + pickleFile,"rb") as f:
			tickers=pickle.load(f) 
		tickers[len(tickers)]=tickerName
		os.remove(data_directory+pickleFile)
		with open(data_directory + pickleFile,"wb") as f:
			pickle.dump(tickers,f)
		print("{} ".format(tickerName)+ "Added to {}".format(pickleFile))

'''
Function Name: remove_ticker_from_pickle(pickleFile, tickerName)
Purpose: This function is used to remove a ticker from a pickle file.
Note: This does not update the data, only the pickle, you should run
	  get_data_from_yahoo() to do so. If you dont use the purge option while
	  doing so, the old data will remain for tickers that no longer exist.
'''

def remove_ticker_from_pickle(pickleFile, tickerName):
	if os.path.exists(data_directory+pickleFile):
		with open(data_directory + pickleFile,"rb") as f:
			tickers=pickle.load(f)
		for i in range (0,len(tickers)):
			if tickers[i]==tickerName:
				print("Removing ticker: {}".format(tickers[i]))
				tickers.drop(labels=i,inplace=True)
		os.remove(data_directory+pickleFile)
		with open(data_directory + pickleFile,"wb") as f:
			pickle.dump(tickers,f)