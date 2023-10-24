import numpy as np
import pandas as pd
import yfinance as yf
import warnings 
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cycler
from matplotlib.dates import MonthLocator, DateFormatter
warnings.filterwarnings("ignore")

# customize graph
colors = cycler('color', 
                ['#669FEE','#66EE91', '#9988DD',
                 '#EECC55', '#88BB44', '#FFBBBB'])
plt.rc('figure', facecolor='#313233')
plt.rc('axes', facecolor='#313233', edgecolor='none',
       axisbelow=True, grid=True, prop_cycle=colors,
       labelcolor='gray')
plt.rc('grid', color='#474A4A', linestyle='solid')
plt.rc('xtick', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('legend', facecolor='#313244', edgecolor='#313233')
plt.rc('text', color='#C9C9C9')

# # open stock ticker
# stick= yf.Ticker("GOOG")
# his=stick.history(period="max")
# print(his)

sticker=yf.download("GOOG")
print(sticker)


# prep the data and format
def preprocessing_yf(symbol):
       # import
       df=yf.download(symbol).dropna()
       
       # rename
       df.columns= ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
       
       # remove adj close
       del df["Adj Close"]
       
       return df

df = preprocessing_yf("GOOG")
print(df)

# Create Simple Moving Average 30 days
df["SMA fast"] = df["Close"].rolling(30).mean()

# Create Simple Moving Average 60 days
df["SMA slow"] = df["Close"].rolling(60).mean()

# Plot Results

fig, ax = plt.subplots(figsize=(15,8))
df[["Close", "SMA fast", "SMA slow"]].loc["2023"].plot(ax=ax)

# change x-axis to month names
ax.xaxis.set_major_locator(MonthLocator())
ax.xaxis.set_major_formatter(DateFormatter("%b"))

# plt.show()

# create empty columns to put signals

df["signal"]=np.nan

# create the condition
condition_buy = (df["SMA fast"] > df["SMA slow"]) & (df["SMA fast"].shift(1) > df["SMA slow"].shift(1))
condition_sell = (df["SMA fast"] < df["SMA slow"]) & (df["SMA fast"].shift(1) < df["SMA slow"].shift(1))

df.loc[condition_buy, "signal"] = 1
df.loc[condition_sell, "signal"] = -1

# plot signals
year = "2023"

# Select signals in index list to plot the points
idx_buy=df.loc[df["signal"] == 1].loc[year].index
idx_sell=df.loc[df["signal"] == -1].loc[year].index

# adapt size of graph
plt.figure(figsize=(30,12))

# color plot points in greeen for buy red for sell
plt.scatter(idx_buy, df.loc[idx_buy]["Close"].loc[year], color="green", marker="^")
plt.scatter(idx_sell, df.loc[idx_sell]["Close"].loc[year], color="red", marker="v")

# plot resistance to ewnsure completions are complete
plt.plot(df["Close"].loc[year].index, df["Close"].loc[year], alpha=0.35)

plt.plot(df["Close"].loc[year].index, df["SMA fast"].loc[year], alpha=0.35)

plt.plot(df["Close"].loc[year].index, df["SMA slow"].loc[year], alpha=0.35)

plt.legend((["Buy", "Sell"], ["GOOG"]))
plt.show()