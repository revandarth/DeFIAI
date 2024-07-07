2. Create a file `src/data_processing/data_processor.py`:

```python
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from src.data_collection.crypto_price_collector import CryptoPriceCollector
from src.data_collection.news_collector import NewsCollector
from datetime import datetime, timedelta

class DataProcessor:
 def __init__(self, db_path='sqlite:///data/crypto_data.db'):
     self.engine = create_engine(db_path)
     self.price_collector = CryptoPriceCollector()
     self.news_collector = NewsCollector()

 def process_price_data(self, coin_id, days=30):
     df = self.price_collector.get_historical_prices(coin_id, days)
     df['date'] = df['timestamp'].dt.date
     df['returns'] = df['price'].pct_change()
     df['volatility'] = df['returns'].rolling(window=7).std() * np.sqrt(365)
     df.dropna(inplace=True)
     return df

 def process_news_data(self, days=30):
     df = self.news_collector.get_crypto_news(days)
     df['date'] = df['publishedAt'].dt.date
     return df

 def merge_data(self, coin_id, days=30):
     price_data = self.process_price_data(coin_id, days)
     news_data = self.process_news_data(days)
     
     merged_data = pd.merge(price_data, news_data, on='date', how='left')
     return merged_data

 def store_data(self, coin_id, days=30):
     data = self.merge_data(coin_id, days)
     data.to_sql(f'{coin_id}_data', self.engine, if_exists='replace', index=False)
     print(f"Data for {coin_id} stored successfully.")

# Usage example
if __name__ == "__main__":
 processor = DataProcessor()
 processor.store_data('ethereum', days=30)