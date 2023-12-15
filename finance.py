import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import yfinance as yf

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

        self.text_ausgabe = tk.Text(self.master, wrap=tk.WORD)
        self.text_ausgabe.pack(expand=True, fill=tk.BOTH)

        self.timer_label = ttk.Label(self.master, text="Nächste Aktualisierung in: -")
        self.timer_label.pack()

        # Initialisierung der Timer-Variable
        self.timer_counter = 0

    def waehrungsdaten_abrufen(self, waehrungseingabe):
        try:
            crypto_ticker = yf.Ticker(waehrungseingabe)
            waehrungsdaten = crypto_ticker.history(period="1d", interval="1h")

            # Daten anzeigen
            self.text_ausgabe.delete(1.0, tk.END)  # Vorherige Daten löschen
            self.text_ausgabe.insert(tk.END, str(waehrungsdaten) + "\n")

            # Timer aktualisieren
            self.timer_counter = 60  # Setze Timer auf 60 Sekunden

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

    def daten_abrufen(self):
        waehrungseingabe = self.waehrung_combobox.get()

        if not waehrungseingabe:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Währung.")
            return

        try:
            # Initiale Daten abrufen
            self.waehrungsdaten_abrufen(waehrungseingabe)

            # Periodischen Datenabruf planen
            self.aktualisiere_daten(waehrungseingabe)

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

    def aktualisiere_daten(self, waehrungseingabe):
        self.waehrungsdaten_abrufen(waehrungseingabe)
        self.timer_counter -= 1

        if self.timer_counter > 0:
            self.timer_label.config(text=f"Nächste Aktualisierung in: {self.timer_counter} Sekunden")
            self.master.after(1000, self.aktualisiere_daten, waehrungseingabe)
        else:
            self.timer_label.config(text="Nächste Aktualisierung in: -")

def main():
    root = tk.Tk()
    foto = tk.PhotoImage(file='appicon.png')
    root.wm_iconphoto(False, foto)
    app = FinanzDatenGUI(root)
    root.geometry("800x600")  # Setze die Anfangsgröße des Fensters
    root.mainloop()

if __name__ == "__main__":
    main()
