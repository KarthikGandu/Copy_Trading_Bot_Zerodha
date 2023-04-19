from setuptools import setup, find_packages

setup(
    name='copy_trading_zerodha',
    version='0.1.0',
    author='Karthik Gandu',
    author_email='gandukarthik1@gmail.com',
    description='''The given program is a GUI application for copy trading of index options on the Zerodha Kite platform. 
    It uses the KiteConnect API to place orders for index options based on user input such as instrument, order type, product, order variety, quantity, stop loss, action, option type, strike price, and target points.
    The program is built using the tkinter library for creating the GUI, and it also uses other libraries such as kite_trade and datetime for interacting with the KiteConnect API.The program allows the user to enter their KiteConnect API access token, and then provides a user-friendly interface for placing orders. It includes dropdown menus for selecting various order parameters, as well as text entry fields for entering quantity, stop loss, strike price, and target points.
    Overall, the program is a useful tool for traders who want to automate their copy trading on the Zerodha Kite platform.''',
    packages=find_packages(),
    install_requires=[
        'kiteconnect',
        'kite_trade',
        'datetime',
        'tkinter',
        'Pillow'
    ],
)
