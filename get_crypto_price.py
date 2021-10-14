# coding: utf8

import time
from tkinter import *
from argparse import ArgumentParser
from random import randint
import requests


class Window:
    def __init__(self):
        self.last_click_x = 0
        self.last_click_y = 0

        self.window = Tk()
        self.price = StringVar()
        self.wallet = StringVar()
        # window.overrideredirect(True)
        self.window.wait_visibility(self.window)
        # window.attributes("-alpha", 0.1)
        self.window.attributes("-topmost", "true")
        self.window.geometry("600x128")
        self.window.wm_attributes("-type", "splash")
        self.window.attributes("-alpha", 0.4)
        self.window.config(bg="black")
        self.window.bind("<Button-1>", self.save_last_click_pos)
        self.window.bind("<B1-Motion>", self.dragging)
        self.window.bind("<Escape>", self.quit)
        self.price_label = Label(
            self.window,
            textvariable=self.price,
            fg="white",
            bg="black",
            font=("Roboto", 24),
        )
        self.wallet_label = Label(
            self.window,
            textvariable=self.wallet,
            fg="white",
            bg="black",
            font=("Roboto", 14),
        )
        self.price_label.pack(anchor=CENTER, expand=True)
        self.wallet_label.pack(anchor=CENTER, expand=True)
        self.running = True
        self.tick = 0

    def save_last_click_pos(self, event):
        self.lastClickX = event.x
        self.lastClickY = event.y

    def get_price(self, currency, symbol, wallet_amount):
        if self.tick % 10 == 0:
            response = requests.get(
                f"https://min-api.cryptocompare.com/data/price?fsym={currency}&tsyms={symbol}"
            )
            if response.status_code == 200:
                price = response.json()
                self.price.set(f"{currency} {str(price[symbol]) } {symbol}")
                self.wallet.set(
                    f"{str(round(wallet_amount * price[symbol], 2))} {symbol}"
                )

    def quit(self, event):
        self.running = False

    def dragging(self, event):
        x, y = (
            event.x - self.last_click_x + self.window.winfo_x(),
            event.y - self.last_click_y + self.window.winfo_y(),
        )
        self.window.geometry("+%s+%s" % (x, y))

    def mainloop(self, currency, symbol, wallet_amount):
        try:
            while self.running:
                self.get_price(currency, symbol, wallet_amount)
                self.window.update_idletasks()
                self.window.update()
                self.tick += 1
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--currency", type=str, default="ETH")
    parser.add_argument("--symbol", type=str, default="EUR")
    parser.add_argument("--wallet-amount", type=float, default=0.0)
    args = parser.parse_args()
    window = Window()
    window.mainloop(args.currency, args.symbol, args.wallet_amount)
