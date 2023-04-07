from binance.client import Client
import numpy as np
from sklearn.linear_model import LinearRegression
import time


class BinancePriceTracker:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(api_key, api_secret)
        self.price_list = []
        self.time_list = []

    def track_price_changes(self):
        try:
            # Get the current ETHUSDT price from Binance API
            price = float(self.client.futures_symbol_ticker(symbol='ETHUSDT')['price'])

            # Append the price and time to their respective lists
            self.price_list.append(price)
            self.time_list.append(time.time())

            # Remove old values that are more than 60 minutes ago
            while self.time_list[-1] - self.time_list[0] > 60 * 60:
                self.price_list.pop(0)
                self.time_list.pop(0)

            # Perform a regression analysis based on the prices and times
            X = np.array(self.time_list).reshape(-1, 1)
            y = np.array(self.price_list)
            reg = LinearRegression().fit(X, y)

            # Calculate the percentage change in price over the last 60 minutes
            percent_change = (self.price_list[-1] - self.price_list[0]) / self.price_list[0] * 100
            print(f'Change {percent_change}')

            # If the percentage change exceeds 1%, output a message to the console
            if abs(percent_change) > 1:
                print(f'Price has changed by {percent_change:.2f}% in the last 60 minutes.')

        except Exception as e:
            print(f'An error occurred: {e}')

    def start_tracking(self):
        # Infinite loop for tracking the price and performing regression analysis
        while True:
            self.track_price_changes()
            # Pause execution for 1 second to avoid excessive load on the server
            time.sleep(1)
