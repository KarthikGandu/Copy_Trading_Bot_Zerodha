import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
#from kite_trade import *
from kiteconnect import KiteConnect, KiteTicker
import datetime


# UI design constants
font_large = ("Helvetica", 14)
font_medium = ("Helvetica", 12)
font_small = ("Helvetica", 10)
bg_color = "#dab10d"  # Light yellow
fg_color = "#2c3e50"  # Dark blue
button_color = "#27ae60"  # Green
label_bg = "#95a5a6"  # Light gray
entry_bg = "#ecf0f1"  # Lighter gray
entry_fg = "#7f8c8d"  # Grayish-blue
menu_bg = "#3498db"  # Light blue
menu_fg = "#ecf0f1"  # Lighter gray


class KiteApp:
    def __init__(self, enctoken):
        self.enctoken = enctoken

    def set_enctoken(self, enctoken):
        self.enctoken = enctoken

    # Add other methods as required


kite1 = KiteApp(enctoken="")
kite2 = KiteApp(enctoken="")


def submit():
    global enctoken1, enctoken2
    enctoken1 = enctoken_entry1.get()
    enctoken2 = enctoken_entry2.get()

    kite1.set_enctoken(enctoken=enctoken1)
    kite2.set_enctoken(enctoken=enctoken2)

    try:
        order_id1 = place_order(kite1)
        order_id2 = place_order(kite2)

        messagebox.showinfo("Success", f"Order placed successfully. Order IDs: {order_id1}, {order_id2}")
    except Exception as e:
        messagebox.showerror("Error", f"Error placing order: {e}")

def place_order(kite_instance):
    lot_sizes = {
    "Nifty": 75,
    "BankNifty": 25,
    "FinNifty": 40
}

    instrument = instrument_var.get()
    order_type = order_type_var.get()
    product = product_var.get()
    order_variety = order_variety_var.get()
    lots = int(quantity_entry.get())
    stop_loss = float(stop_loss_entry.get())
    action = action_var.get()
    option_type = option_type_var.get()
    strike_price = float(strike_price_entry.get())
    target_points = float(target_entry.get())

    lot_size = lot_sizes[instrument]
    quantity = lots * lot_size

    tradingsymbol = f"{instrument}{strike_price:.2f}{option_type}"
    trading_weekly_symbol = get_weekly_symbol(kite_instance, tradingsymbol)

    price = get_price(kite_instance, trading_weekly_symbol)
    trigger_price = price - stop_loss
    target_price = price + target_points

    order_id = kite_instance.place_order(
        variety=order_variety.lower(),
        exchange=kite_instance.EXCHANGE_NFO,
        tradingsymbol=trading_weekly_symbol,
        transaction_type=kite_instance.TRANSACTION_TYPE_BUY,
        quantity=quantity,
        price=None if order_type == "MARKET" else stop_loss,
        product=product,
        order_type=kite_instance.ORDER_TYPE_MARKET if order_type == "MARKET" else kite_instance.ORDER_TYPE_LIMIT,
        validity=kite_instance.VALIDITY_DAY,
        disclosed_quantity=None if order_variety == "Regular" else int(quantity * 0.1),
        trigger_price=None if order_type != "STOPLOSS" else trigger_price,
        squareoff=None,
        stoploss=None,
        trailing_stoploss=None,
        tag=None,
    )

    return order_id


def get_expiry_date(kite_instance, instrument):
    expiries = kite_instance.ltp(f"NSE:{instrument}").keys()
    expiry_dates = [datetime.datetime.strptime(expiry.split(" ")[-1], "%Y-%m-%d") for expiry in expiries]
    return min(expiry_dates).strftime("%Y-%m-%d")

def get_weekly_symbol(kite_instance, tradingsymbol):
    instrument = tradingsymbol[:-2]
    expiry_date = get_expiry_date(kite_instance, instrument)
    weekly_symbol = f"{tradingsymbol}:{expiry_date}"
    return weekly_symbol

def get_price(kite_instance, tradingsymbol):
    ltp_data = kite_instance.ltp(tradingsymbol)
    price = ltp_data[tradingsymbol]['last_price']
    return price


root = tk.Tk()
root.title("Copy Trading FOR Zerodha Kite Index Options")

root.geometry("400x500")


# Create widgets
enctoken_label1 = tk.Label(root, text="Enctoken 1")
enctoken_entry1 = tk.Entry(root)

enctoken_label2 = tk.Label(root, text="Enctoken 2")
enctoken_entry2 = tk.Entry(root)

instrument_label = tk.Label(root, text="Instrument")
instrument_var = tk.StringVar()
instrument_options = ["Nifty", "BankNifty", "FinNifty"]
instrument_menu = ttk.OptionMenu(root, instrument_var, instrument_options[0], *instrument_options)

order_type_label = tk.Label(root, text="Order Type")
order_type_var = tk.StringVar()
order_type_options = ["MARKET", "LIMIT", "STOPLOSS"]
order_type_menu = ttk.OptionMenu(root, order_type_var, order_type_options[0], *order_type_options)

product_label = tk.Label(root, text="Product")
product_var = tk.StringVar()
product_options = ["CNC", "MIS", "NRML"]
product_menu = ttk.OptionMenu(root, product_var, product_options[0], *product_options)

order_variety_label = tk.Label(root, text="Order Variety")
order_variety_var = tk.StringVar()
order_variety_options = ["Regular", "Iceberg"]
order_variety_menu = ttk.OptionMenu(root, order_variety_var, order_variety_options[0], *order_variety_options)

quantity_label = tk.Label(root, text="Quantity")
quantity_entry = tk.Entry(root)

stop_loss_label = tk.Label(root, text="Stop Loss")
stop_loss_entry = tk.Entry(root)

action_label = tk.Label(root, text="Action")
action_var = tk.StringVar()
action_options = ["BUY", "SELL"]
action_menu = ttk.OptionMenu(root, action_var, action_options[0], *action_options)

option_type_label = tk.Label(root, text="Option Type")
option_type_var = tk.StringVar()
option_type_options = ["CE", "PE"]
option_type_menu = ttk.OptionMenu(root, option_type_var, option_type_options[0], *option_type_options)

strike_price_label = tk.Label(root, text="Strike Price")
strike_price_entry = tk.Entry(root)

target_label = tk.Label(root, text="Target Points")
target_entry = tk.Entry(root)

submit_button = tk.Button(root, text="Submit", command=submit)

##updated
# Create a style object and configure the TMenubutton style
style = ttk.Style()
style.configure("TMenubutton.dropdown", background=menu_bg, foreground=menu_fg, font=font_medium)
style.map("TMenubutton.dropdown",
          fieldbackground=[("readonly", menu_bg), ("!disabled", menu_bg)],
          selectbackground=[("readonly", menu_bg), ("!disabled", menu_bg)],
          selectforeground=[("readonly", menu_fg), ("!disabled", menu_fg)])

# Modify the widgets to apply colors and fonts
# Modify the widgets to apply colors and fonts
for widget in (enctoken_label1, enctoken_label2, instrument_label, order_type_label, product_label, order_variety_label,
               quantity_label, stop_loss_label, action_label, option_type_label, strike_price_label, target_label):
    widget.config(bg=label_bg, fg=fg_color, font=font_medium)

for entry in (enctoken_entry1, enctoken_entry2, quantity_entry, stop_loss_entry, strike_price_entry, target_entry):
    entry.config(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, font=font_medium)

instrument_menu = ttk.OptionMenu(root, instrument_var, instrument_options[0], *instrument_options, style="TMenubutton")
order_type_menu = ttk.OptionMenu(root, order_type_var, order_type_options[0], *order_type_options, style="TMenubutton")
product_menu = ttk.OptionMenu(root, product_var, product_options[0], *product_options, style="TMenubutton")
order_variety_menu = ttk.OptionMenu(root, order_variety_var, order_variety_options[0], *order_variety_options, style="TMenubutton")
action_menu = ttk.OptionMenu(root, action_var, action_options[0], *action_options, style="TMenubutton")
option_type_menu = ttk.OptionMenu(root, option_type_var, option_type_options[0], *option_type_options, style="TMenubutton")

submit_button.config(bg=button_color, fg=fg_color, font=font_medium)

root.config(bg=bg_color)


# Place widgets
enctoken_label1.grid(row=0, column=0)
enctoken_entry1.grid(row=0, column=1)

enctoken_label2.grid(row=1, column=0)
enctoken_entry2.grid(row=1, column=1)

instrument_label.grid(row=2, column=0)
instrument_menu.grid(row=2, column=1)

order_type_label.grid(row=3, column=0)
order_type_menu.grid(row=3, column=1)

product_label.grid(row=4, column=0)
product_menu.grid(row=4, column=1)

order_variety_label.grid(row=5, column=0)
order_variety_menu.grid(row=5, column=1)

quantity_label.grid(row=6, column=0)
quantity_entry.grid(row=6, column=1)

stop_loss_label.grid(row=7, column=0)
stop_loss_entry.grid(row=7, column=1)

action_label.grid(row=8, column=0)
action_menu.grid(row=8, column=1)

option_type_label.grid(row=9, column=0)
option_type_menu.grid(row=9, column=1)

strike_price_label.grid(row=10, column=0)
strike_price_entry.grid(row=10, column=1)

target_label.grid(row=11, column=0)
target_entry.grid(row=11, column=1)

submit_button.grid(row=12, column=0, columnspan=2)

# Run the main loop
root.mainloop()