import numpy as np
import pandas as pd
import yfinance as yf
import warnings 
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cycler
warnings.filterwarnings("ignore")

# customize graph
colors = cycler('color', 
                ['#669FEE','#66EE91', '#9988DD',
                 '#EECC55', '#88BB44', '#FFBBBB'])
plt.rc('figure', facecolor='#313233')
plt.rc('axes', facecolor='#313233', edgecolor='none',
       axisbelow=True, grid=True, prop_cycle=colors,
       labelcolor='gray')
plt.rc('grid', color='474A4A', linestyle='solid')
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

df[["close", "SMA fast", "SMA slow"]].loc["2020"].plot(figsize=(15,8))
