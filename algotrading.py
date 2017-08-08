import matplotlib
import matplotlib.axes as axes
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from mayavi import mlab
from mayavi.mlab import *
import numpy as np


from matplotlib import style
import pandas as pd
import pandas_datareader as web
import datetime as dt
import quandl


# df=quandl.get("FB", start_date="2016-05-19")

#

start=dt.datetime(2000,1,1)
end=dt.datetime.today()
df=web.DataReader('tsla','google',start,end)
print (df.head(6))
df.to_csv('tsla.csv')
#######################################################################
df=pd.read_csv('tsla.csv',parse_dates=True,index_col=0)
df.dropna(inplace=True)

# df_ohlc=df['Close'].resample('1D').ohlc()
# df_volume=df['Total Trade Quantity'].resample('1D').sum()
# df_ohlc.reset_index(inplace=True)
# df_ohlc['Date']=df_ohlc['Date'].map(mdates.date2num)
# df_ohlc.dropna(inplace=True)
ax1=plt.subplot()
# candlestick_ohlc(ax1,df_ohlc.values,width=0.6,colorup='g')
# ax1.xaxis_date()

######################################################################
#
df['tankensen']=(df['High'].rolling(window=9).max()+df['Low'].rolling(window=9).min())/2
df['kejunsen']=(df['High'].rolling(window=26).max()+df['Low'].rolling(window=26).min())/2
# df.dropna(inplace=True)
ax1.plot(df['tankensen'])
ax1.plot(df['kejunsen'])

# print(df['Date'])
# plt.show()

#
df['senkuspanA']=(df['tankensen']+df['kejunsen'])/2
df['senkuspanB']=(df['High'].rolling(window=52).max()+df['Low'].rolling(window=52).min())/2
df['senkuspanA']=df['senkuspanA'].shift(26)
df['senkuspanB']=df['senkuspanB'].shift(26)
df['currentprice']=(df['High'] +df['Low'])/2
# df.dropna(inplace=True)
ax1.plot(df['senkuspanA'])
ax1.plot(df['senkuspanB'])
# ax1.plot(df['currentprice'])
ax1.fill_between(df.index,y1=df['senkuspanA'],y2=df['senkuspanB'],color='green',where=df['senkuspanA'] >= df['senkuspanB'])
ax1.fill_between(df.index,y1=df['senkuspanA'],y2=df['senkuspanB'],color='red',where=df['senkuspanA'] <= df['senkuspanB'])

df['Buy/Sell']=(df['senkuspanA']>df['senkuspanB']) & (df['tankensen']>df['kejunsen']) &(df['currentprice']>df['senkuspanA'])
# ax1.scatter(df['currentprice'],df['Date'] ,label='signal', c='b')
ax1.legend(['t','k','sA','sB','cp'],loc='upper left')

# for i in df['Buy/Sell']:
#     if (df['senkuspanA']>df['senkuspanB']):
#         df['Buy/Sell']='Buy'
#     elif(df['senkuspanA']<df['senkuspanB']):
#         df['Buy/Sell']='Sell'
# df.to_csv('ORCL2.csv')
print(df)
# df.to_csv('bomf.csv')

plt.show()
