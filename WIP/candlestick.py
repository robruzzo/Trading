# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 19:39:36 2020

@author: robru
"""

import datetime as dt
import pandas as pd
import pandas_datareader.data as web
from plotly.offline import plot
import plotly.graph_objects as go

df= pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

df=df[-60:]

#Resample will recalcuate a value and save it 10 days
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)  


fig1 = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Adj Close'])])

fig1.update_layout(xaxis_rangeslider_visible=False)

plot(fig1)

fig2 = go.Figure(data=[go.Candlestick(x=df_ohlc['Date'],
                open=df_ohlc['open'],
                high=df_ohlc['high'],
                low=df_ohlc['low'],
                close=df_ohlc['close'])])

fig2.update_layout(xaxis_rangeslider_visible=False)
plot(fig2)

