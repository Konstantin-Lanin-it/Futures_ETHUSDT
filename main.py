from config import YOUR_API_KEY, YOUR_API_SECRET
from price_tracker import BinancePriceTracker
from price_analyzer import ETHPriceAnalyzer


def eth_price_analyzer(api_key, api_secret):
    analyzer = ETHPriceAnalyzer(api_key, api_secret)

    # Get the percentage price changes of ETHUSDT and BTCUSDT futures
    eth_price_changes = analyzer.get_price_changes('ETHUSDT')
    btc_price_changes = analyzer.get_price_changes('BTCUSDT')

    # Exclude the influence of BTCUSDT futures on the price changes of ETHUSDT futures
    eth_price_changes_no_btc = analyzer.exclude_btc_influence(eth_price_changes, btc_price_changes)

    return eth_price_changes_no_btc


def binance_price_tracker(api_key, api_secret):
    tracker = BinancePriceTracker(api_key, api_secret)
    tracker.start_tracking()


if __name__ == 'main':
    print('ETH price changes:', eth_price_analyzer(YOUR_API_KEY, YOUR_API_SECRET))
    binance_price_tracker(YOUR_API_KEY, YOUR_API_SECRET)
