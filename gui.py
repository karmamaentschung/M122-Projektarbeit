#--
#
#
#
#--

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sched
import time
import yfinance as yf
import pandas as pd

class FinanceDataGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Finance Tracker")

        self.currency_label = ttk.Label(self.master, text="Choose a crypto currency or stock:")
        self.currency_label.pack()

        self.currency_combobox = ttk.Combobox(self.master, values=["BTC-USD", "XRP-USD", "ETH-USD", "BLK", "ROG", "TSLA"])
        self.currency_combobox.pack()

        self.get_data_button = ttk.Button(self.master, text="Get Data", command=self.get_data)
        self.get_data_button.pack()

        self.text_output = tk.Text(self.master, wrap=tk.WORD)
        self.text_output.pack(expand=True, fill=tk.BOTH)

    def get_currency_data(self, currency_input):
        try:
            crypto_ticker = yf.Ticker(currency_input)
            currency_data = crypto_ticker.history(period="1d", interval="1h")

            # Display the data
            self.text_output.insert(tk.END, str(currency_data) + "\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def get_data(self):
        currency_input = self.currency_combobox.get()

        if not currency_input:
            messagebox.showwarning("Warning", "Please choose a currency.")
            return

        try:
            # Get initial data
            ticker = yf.Ticker(currency_input)
            temp_data = ticker.history(period="1d", interval="1m")
            self.text_output.insert(tk.END, str(temp_data) + "\n")

            # Schedule periodic data retrieval
            my_scheduler = sched.scheduler(time.time, time.sleep)
            my_scheduler.enter(60, 1, self.get_currency_data, (currency_input,))
            my_scheduler.run()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    app = FinanceDataGUI(root)
    root.geometry("800x600")  # Set the initial size of the window
    root.mainloop()

if __name__ == "__main__":
    main()