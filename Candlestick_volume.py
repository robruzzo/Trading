# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:17:19 2020

@author: robru
"""


import pandas as pd
from plotly.subplots import make_subplots
from plotly.offline import plot
import plotly.graph_objects as go

df= pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

df=df[-60:]

fig = make_subplots(rows=2, cols=1, row_heights=[0.9,0.1], subplot_titles=["Tesla OHLC","Daily Volume"])


fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Adj Close']),row=1,col=1)

fig.add_trace(go.Bar(x=df.index,
                y=df['Volume']),row=2,col=1)

fig.update_layout(xaxis_rangeslider_visible=False,showlegend=False,width=900, height=900)

plot(fig)
fig.show()

