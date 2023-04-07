from binance.client import Client
import numpy as np
from sklearn.linear_model import LinearRegression


class ETHPriceAnalyzer:
    def __init__(self, api_key, api_secret):
        # Initialize Binance client using API key and secret
        self.client = Client(api_key, api_secret)

    def get_price_changes(self, symbol):
        # Get historical data for a given symbol (ETHUSDT or BTCUSDT) and calculate percentage price changes
        klines = self.client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, limit=1000)
        price_changes = []
        for i in range(1, len(klines)):
            prev_close = float(klines[i - 1][4])
            curr_close = float(klines[i][4])
            price_change = (curr_close - prev_close) / prev_close * 100
            price_changes.append(price_change)
        return price_changes

    def exclude_btc_influence(self, eth_price_changes, btc_price_changes):
        # Use linear regression to model the influence of BTC price changes on ETH price changes and remove that influence
        model = LinearRegression()
        X = np.array(btc_price_changes).reshape(-1, 1)
        y = np.array(eth_price_changes)
        model.fit(X, y)
        y_pred = model.predict(X)
        eth_price_changes_no_btc = y - y_pred
        return
