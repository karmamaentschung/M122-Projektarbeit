#!/usr/bin/python3

# ------------------------------------------------------------------
# Name  : algorythm.py
#
# Description: Trading Algorythm | USE TREND-Following Algorythm for the trading bot!!!
#
# Autor: Florin Curiger
#
# ------------------------------------------------------------------



def initialize(state):
    pass



@schedule (interval="1h", symbol="ETHUSDT")
def handler(state, data):

    #Compute indicators
    ema_30 = data.ema(30).last
    ema_100 = data.ema(100).last
    
    if ema_100 is None:
        return
    
    # Fetch portfolio
    portfolio = query_portfolio()
    balance_quoted = portfolio.excess_liquidity_quoted
    buy_value = float(balance_quoted) * 0.2

    # Fetch position
    position = query_open_position_by_symbol(data.symbol, include_dust=False)
    has_position = position is not None
    

    #Buy & Sell signals
    if ema_30 > ema_100 and not has_position:
        order_market_value(symbol=data.symbol, value=buy_value)
    elif ema_30 < ema_100 and has_position:
        close_position(data.symbol)

