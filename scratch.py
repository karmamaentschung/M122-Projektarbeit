import sched
import time
import yfinance as yf

print("""Please choose between the following Crypto currencies to get the data from:
-- Cryptocurrencies --
BTC-USD
XRP-USD
ETH-USD
-- STOCKS--
BLK
ROG
TSLA
""")
currency_input = input("Enter the Currency from which you want to get the current values:   ")

def get_currency_Data(scheduler):
    # Schedule the next call first
    scheduler.enter(60, 1, get_currency_Data, (scheduler,))

    crypto_Ticker = yf.Ticker(currency_input)
    currency_Data = crypto_Ticker.history(period="max")

    print(currency_Data)


ticker = yf.Ticker(currency_input)
temp_data = ticker.history(period="max")
print(temp_data)
my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(60, 1, get_currency_Data, (my_scheduler,))
my_scheduler.run()
