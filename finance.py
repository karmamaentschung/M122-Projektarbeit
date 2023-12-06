#!/usr/bin/python
#Autoren: Florin Curiger, Enrique Munoz und Karma Khamritshang
#-------------------------------------------------------------

import yfinance as yf

BTC_Ticker = yf.Ticker("BTC-USD")
BTC_Data = BTC_Ticker.history(period="max")

print(BTC_Data)
