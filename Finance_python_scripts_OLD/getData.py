# import yfinance as yf
# Imports for pandas_datareader
# import pandas_datareader.data as web
import pandas as pd
# Imports for 
import os
from datetime import datetime
import requests
import nasdaqdatalink


"""
url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=5XJ2EIIMEWPWIIYK'
r = requests.get(url)
dataF = r.json()

print(data)
"""
data = 'C://Users/flori/OneDrive/Dokumente/00_ZLI/17_Abschlussarbeit/abschlussarbeit_ZLI/01_SourceCode/ETH-USD.csv'

eth_bars = pd.read_csv(data)
eth_bars

dataF = pd.DataFrame(eth_bars)

print(dataF)


"""
def signal_generator(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]
    
    # Bearish Pattern
    if (open>close and 
    previous_open<previous_close and 
    close<previous_open and
    open>=previous_close):
        return 1

    # Bullish Pattern
    elif (open<close and 
        previous_open>previous_close and 
        close>previous_open and
        open<=previous_close):
        return 2
    
    # No clear pattern
    else:
        return 0

signal = []
signal.append(0)
for i in range(1,len(dataF)):
    df = dataF[i-1:i+1]
    signal.append(signal_generator(df))
#signal_generator(data)
dataF["signal"] = signal


dataF.signal.value_counts()
#dataF.iloc[:, :]
"""

