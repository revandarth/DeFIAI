from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime, timedelta

class CryptoPriceCollector:
 def __init__(self):
     self.cg = CoinGeckoAPI()

 def get_historical_prices(self, coin_id, days):
     data = self.cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=days)
     df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
     df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
     return df

 def get_current_price(self, coin_id):
     data = self.cg.get_price(ids=coin_id, vs_currencies='usd')
     return data[coin_id]['usd']

# Usage example
if __name__ == "__main__":
 collector = CryptoPriceCollector()
 
 # Get historical prices for Ethereum for the last 30 days
 eth_prices = collector.get_historical_prices('ethereum', 30)
 print(eth_prices.head())

 # Get current price for Ethereum
 eth_current_price = collector.get_current_price('ethereum')
 print(f"Current Ethereum price: ${eth_current_price}")