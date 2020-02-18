# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

df= pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

#Calculate the 100 day moving averatge

df['100ma']=df['Adj Close'].rolling(window=100, min_periods=0).mean()

"""
Create a Plot of the 100 day moving average, with the adjusted close and 
the volume as a bar graph at the bottom. Set shareax in order to make it so
that when the top is zoomed the bottom is zoomed. The graph will be 6 rows, 5
will be the top part and 1 row will be the bar graph.
"""

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])
plt.show()