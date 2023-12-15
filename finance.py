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
        self.master.title("Finanz Tracker - Modul 122")

        self.waehrung_label = ttk.Label(self.master, text="Wählen Sie eine Krypto-Währung oder Aktie:")
        self.waehrung_label.pack()

        self.waehrung_combobox = ttk.Combobox(self.master, values=["BTC-USD", "XRP-USD", "ETH-USD", "BLK", "ROG", "TSLA"])
        self.waehrung_combobox.pack()

        self.daten_abrufen_button = ttk.Button(self.master, text="Daten abrufen", command=self.daten_abrufen)
        self.daten_abrufen_button.pack()
        
        self.verlassen_button = ttk.Button(self.master, text="Verlassen", command=self.master.quit)
        self.verlassen_button.pack()

        self.text_ausgabe = tk.Text(self.master, wrap=tk.WORD)
        self.text_ausgabe.pack(expand=True, fill=tk.BOTH)

        self.timer_label = ttk.Label(self.master, text="Nächste Aktualisierung in: -")
        self.timer_label.pack()
        
        self.progressbar = ttk.Progressbar(self.master, orient="horizontal", mode="determinate", length=200)
        self.progressbar.pack()

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

            # Fortschrittsbalken aktualisieren
            self.progressbar["value"] = 0  # Zurücksetzen des Fortschrittsbalkens

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

    def daten_abrufen(self):
        waehrungseingabe = self.waehrung_combobox.get()

        if not waehrungseingabe:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Währung.")
            return

        try:
            # Initiale Daten abrufen
            self.waehrungsdaten_abrufen(waehrungseingabe, period="1h", interval="1m")

            # Timer starten oder neu starten
            if self.timer_id is not None:
               self.master.after_cancel(self.timer_id)
            self.starte_timer(waehrungseingabe)

            # Fortschrittsbalken starten
            self.starte_fortschrittsbalken()

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

    def starte_timer(self, waehrungseingabe):
        # Timer starten oder neu starten
        self.timer_counter = 60
        self.aktualisiere_timer_label()
        self.timer_id = self.master.after(1000, self.aktualisiere_timer, waehrungseingabe)

    def starte_fortschrittsbalken(self):
        self.progressbar["maximum"] = 60  # Maximale Zeit für den Fortschrittsbalken in Sekunden
        self.progressbar["value"] = 0
        self.aktualisiere_fortschrittsbalken()

    def aktualisiere_timer(self, waehrungseingabe):
        self.timer_counter -= 1
        self.aktualisiere_timer_label()

        if self.timer_counter <= 0:
            # Timer abgelaufen, Daten aktualisieren und Timer neu starten
            self.waehrungsdaten_abrufen(waehrungseingabe, period="1d", interval="1m")
            self.starte_timer(waehrungseingabe)

            # Fortschrittsbalken starten
            self.starte_fortschrittsbalken()
        else:
            # Timer weiter aktualisieren
            self.timer_id = self.master.after(1000, self.aktualisiere_timer, waehrungseingabe)

    def aktualisiere_timer_label(self):
        self.timer_label.config(text=f"Nächste Aktualisierung in: {self.timer_counter} Sekunden")

    def aktualisiere_fortschrittsbalken(self):
        current_value = self.progressbar["value"]
        if current_value < self.progressbar["maximum"]:
            self.progressbar["value"] += 1
            self.master.after(1000, self.aktualisiere_fortschrittsbalken)
        else:
            # Fortschrittsbalken zurücksetzen
            self.progressbar["value"] = 0

    def manuelle_aktualisierung(self):
        waehrungseingabe = self.waehrung_combobox.get()
        self.waehrungsdaten_abrufen(waehrungseingabe, period="1d", interval="1m")

def main():
    root = tk.Tk()
    foto = tk.PhotoImage(file='appicon.png')
    root.wm_iconphoto(False, foto)
    app = FinanzDatenGUI(root)
    root.geometry("900x650")  # Setze die Anfangsgrösse des Fensters
    root.mainloop()


if __name__ == "__main__":
    main()
