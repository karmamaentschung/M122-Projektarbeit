import sched
import time
import yfinance as yf
import pandas as pd

def get_currency_data(scheduler, currency_input):
    try:
        # Schedule the next call first
        scheduler.enter(60, 1, get_currency_data, (scheduler, currency_input))

        crypto_ticker = yf.Ticker(currency_input)
        currency_data = crypto_ticker.history(period="1d", interval="1h")

        # Display the data
        print(currency_data)

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
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
    
    while True:
        currency_input = input("Enter the Currency from which you want to get the current values:   ")
        
        valid_currencies = ["BTC-USD", "XRP-USD", "ETH-USD", "BLK", "ROG", "TSLA"]
        if currency_input in valid_currencies:
            break
        else:
            print("Invalid currency entered. Please choose a valid currency.")

    # Get initial data
    ticker = yf.Ticker(currency_input)
    temp_data = ticker.history(period="1d", interval="1h")
    print(temp_data)

    # Schedule periodic data retrieval
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(60, 1, get_currency_data, (my_scheduler, currency_input))
    my_scheduler.run()

if __name__ == "__main__":
    main()
