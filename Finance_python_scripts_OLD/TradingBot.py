'''
In this bot template the possibility to use different symbols is represented.
If you are new and trying to get started we recommend checking our https://app.trality.com/masterclass
For more information on each part of a trading bot, please visit our documentation pages: https://docs.trality.com
The selection of the given symbols in this example is arbitrary. This could have been made following some data analyses or
i.e. analyzing the correlations between these two symbols.
The logic is simple: a general signal is computed for each asset used in this bot,
and orders are made for a single asset in case the signal agrees for all symbols,
In this example, we use a combination of EMA crossover and RSI, and invest roughly half our portfolio
into a single asset.
'''

SYMBOLS = ["BTCBUSD", "ETHBUSD"]

SIGNAL_BUY = 1
SIGNAL_SELL = 2
SIGNAL_IGNORE = 3

def initialize(state):
   state.signals = {}  # This is where signals will be stored for each symbol
   state.signal_parameters = [20, 40, 14]

# Compute a signal for a specific symbol pair
def compute_signal(data, short_n, long_n, rsi_n):
    # Computing indicators from data
    ema_short_ind = data.ema(short_n)
    ema_long_ind = data.ema(long_n)
    rsi_ind = data.rsi(rsi_n)

    # On erroneous data return early (indicators are of NoneType)
    if ema_short_ind is None or ema_long_ind is None or rsi_ind is None:
        return

    ema_short = ema_short_ind.last  # Getting latest value for ema_short from data object
    ema_long = ema_long_ind.last
    rsi = rsi_ind.last

    if ema_short > ema_long and rsi < 35:
        signal = SIGNAL_BUY
    elif ema_short < ema_long and rsi > 65:
        signal = SIGNAL_SELL
    else:
        signal = SIGNAL_IGNORE
    return signal

# Store signal in state
def resolve_ema_signal(state, data):
    state.signals[data.symbol] = compute_signal(data, *state.signal_parameters)

# Check if all signals agree
def resolve_action(state):
    signals = list(state.signals.values())
    if all(x == SIGNAL_BUY for x in signals):
        return SIGNAL_BUY
    elif all(x == SIGNAL_SELL for x in signals):
        return SIGNAL_SELL
    else:
        return SIGNAL_IGNORE

@schedule(interval= "15m", symbol=SYMBOLS)
def handler(state, dataMap):

    # Resolve all signals
    for symbol, data in dataMap.items():
        resolve_ema_signal(state, data)

    # Resolve action
    action = resolve_action(state)

    # Skip early
    if action == SIGNAL_IGNORE:
        return

    # Let's say we're buying/selling ETH if BTC agrees
    data = dataMap[SYMBOLS[1]]

    print("Resolved {} signal for {}".format("BUY" if action is SIGNAL_BUY else "SELL", data.symbol))

    # This code block is querying the portfolio to see if it has any open positions,
    # querying the amount of quoted balance we have free
    # and the amount of the traded asset that we have free.
    has_position = has_open_position(data.symbol, include_dust=False)
    balance_base = float(query_balance_free(data.base))
    balance_quoted = float(query_balance_free(data.quoted))
    buy_amount = balance_quoted / data.close_last * 0.5

    # Depending on given signals sets buy or sell order
    if action == SIGNAL_BUY and balance_base<buy_amount and not has_position:
        print("-> Buying {}".format(data.symbol))
        order_market_amount(symbol=data.symbol,amount=buy_amount)
    elif action == SIGNAL_SELL and has_position:
        print("-> Selling {}".format(data.symbol))
        close_position(data.symbol)
