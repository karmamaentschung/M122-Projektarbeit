#!/usr/bin/python
################################################################
# Datei: finance.py  
# Autoren: Enrique Munoz, Florin Curiger und Karma Khamritshang
################################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import yfinance as yf
from datetime import datetime, timedelta
import pytz

class FinanzDatenGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Finanz Tracker")

        self.waehrung_label = ttk.Label(self.master, text="Wählen Sie eine Krypto-Währung oder Aktie:")
        self.waehrung_label.pack()

        self.waehrung_combobox = ttk.Combobox(self.master, values=["BTC-USD", "XRP-USD", "ETH-USD", "BLK", "ROG", "TSLA"])
        self.waehrung_combobox.pack()

        self.daten_abrufen_button = ttk.Button(self.master, text="Daten abrufen", command=self.daten_abrufen)
        self.daten_abrufen_button.pack()

        self.verlassen_button = ttk.Button(self.master, text="Verlassen", command=self.master.destroy)
        self.verlassen_button.pack()

        self.text_ausgabe = tk.Text(self.master, wrap=tk.WORD)
        self.text_ausgabe.pack(expand=True, fill=tk.BOTH)

        self.progress_bar = ttk.Progressbar(self.master, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.pack()

        self.timer_label = ttk.Label(self.master, text="Nächste Aktualisierung in: -")
        self.timer_label.pack()

        # Zeitzone für Bern, Schweiz
        self.berlin_tz = pytz.timezone('Europe/Zurich')

        # Timer-Variable initialisieren
        self.timer_counter = 60
        self.timer_id = None

    def waehrungsdaten_abrufen(self, waehrungseingabe, period="1d", interval="1h"):
        try:
            crypto_ticker = yf.Ticker(waehrungseingabe)
            waehrungsdaten = crypto_ticker.history(period=period, interval=interval)

            # Daten anzeigen
            self.text_ausgabe.delete(1.0, tk.END)  # Vorherige Daten löschen
            self.text_ausgabe.insert(tk.END, str(waehrungsdaten) + "\n")

            # Timer-Label aktualisieren
            self.aktualisiere_timer_label()

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

    def daten_abrufen(self):
        waehrungseingabe = self.waehrung_combobox.get()

        if not waehrungseingabe:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Währung.")
            return

        try:
            # Initiale Daten abrufen
            self.start_progress_bar()
            self.waehrungsdaten_abrufen(waehrungseingabe, period="1d", interval="1m")

            # Timer starten oder neu starten
            if self.timer_id is not None:
                self.master.after_cancel(self.timer_id)
            self.starte_timer(waehrungseingabe)

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")
        finally:
            self.stop_progress_bar()

    def starte_timer(self, waehrungseingabe):
        # Timer starten oder neu starten
        self.timer_counter = 60
        self.aktualisiere_timer_label()
        self.timer_id = self.master.after(1000, self.aktualisiere_timer, waehrungseingabe)

    def aktualisiere_timer(self, waehrungseingabe):
        self.timer_counter -= 1
        self.aktualisiere_timer_label()

        if self.timer_counter <= 0:
            # Timer abgelaufen, Daten aktualisieren und Timer neu starten
            self.waehrungsdaten_abrufen(waehrungseingabe, period="1d", interval="1m")
            self.starte_timer(waehrungseingabe)
        else:
            # Timer weiter aktualisieren
            self.timer_id = self.master.after(1000, self.aktualisiere_timer, waehrungseingabe)

    def aktualisiere_timer_label(self):
        self.timer_label.config(text=f"Nächste Aktualisierung in: {self.timer_counter} Sekunden")

    def start_progress_bar(self):
        self.progress_bar.start()

    def stop_progress_bar(self):
        self.progress_bar.stop()


def main():
    root = tk.Tk()
    foto = tk.PhotoImage(file='appicon.png')
    root.wm_iconphoto(False, foto)
    app = FinanzDatenGUI(root)
    root.geometry("800x600")  # Setze die Anfangsgröße des Fensters
    root.mainloop()


if __name__ == "__main__":
    main()
