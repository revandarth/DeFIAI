from newsapi import NewsApiClient
import pandas as pd
from datetime import datetime, timedelta

class NewsCollector:
    def __init__(self, api_key):
        self.newsapi = NewsApiClient(api_key=api_key)

    def get_crypto_news(self, days=7):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        articles = self.newsapi.get_everything(q='cryptocurrency OR bitcoin OR ethereum',
                                               from_param=start_date.strftime('%Y-%m-%d'),
                                               to=end_date.strftime('%Y-%m-%d'),
                                               language='en',
                                               sort_by='relevancy')

        df = pd.DataFrame(articles['articles'])
        df['publishedAt'] = pd.to_datetime(df['publishedAt'])
        return df

# Usage example
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')

    collector = NewsCollector(NEWS_API_KEY)
    news_df = collector.get_crypto_news()
    print(news_df.head())