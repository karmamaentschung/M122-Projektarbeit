#!/usr/bin/python3

# ------------------------------------------------------------------
# Name  : simple_macd_strategy.py
#
# Description: Trading Bot using Trality
#
# Autor: Florin Curiger
#
# ------------------------------------------------------------------

# MACD = EMA_12 - EMA_26 of price
# MACD Signal = EMA_9 of MACD

def initialize(state):
    pass


@schedule(interval="1h", symbol="BTCUSDT")
def handler(state, data):

    macd_ind = data.macd(12, 26 , 9)

    if macd_ind is None:
        return

    macd = macd_ind['macd'].last # EMA_12 - EMA_26
    macd_signal = macd_ind['macd_signal'].last # EMA_9 of macd

    current_price = data.close_last

    # Fetch Portfolio

    portfolio = query_portfolio()
    balance_quoted = portfolio.excess_liquidity_quoted
    buy_value = float(balance_quoted) * 0.6

    # Fetch position

    position = query_open_position_by_symbol(data.symbol, include_dust=False)
    has_position = position is not None

    # Buy & Sell Signals

    if macd > macd_signal and not has_position:
        order_market_value(symbol=data.symbol, value=buy_value)
    elif macd < macd_signal and has_position:
        close_position(data.symbol)

