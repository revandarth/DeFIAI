from transformers import pipeline
import pandas as pd
from sqlalchemy import create_engine

class SentimentAnalyzer:
 def __init__(self, db_path='sqlite:///data/crypto_data.db'):
     self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
     self.engine = create_engine(db_path)

 def analyze_sentiment(self, text):
     result = self.sentiment_pipeline(text[:512])[0]  # Limit text to 512 tokens
     return result['label'], result['score']

 def process_news_sentiment(self, coin_id):
     query = f"SELECT * FROM {coin_id}_data WHERE title IS NOT NULL"
     df = pd.read_sql(query, self.engine)
     
     df['sentiment_label'], df['sentiment_score'] = zip(*df['title'].apply(self.analyze_sentiment))
     df['sentiment_numeric'] = df['sentiment_label'].map({'POSITIVE': 1, 'NEGATIVE': -1})
     df['weighted_sentiment'] = df['sentiment_numeric'] * df['sentiment_score']
     
     # Calculate daily average sentiment
     daily_sentiment = df.groupby('date')['weighted_sentiment'].mean().reset_index()
     daily_sentiment.columns = ['date', 'avg_sentiment']
     
     # Merge back with the original data
     result = pd.merge(df, daily_sentiment, on='date', how='left')
     
     # Update the database with sentiment data
     result.to_sql(f'{coin_id}_data', self.engine, if_exists='replace', index=False)
     print(f"Sentiment analysis for {coin_id} completed and stored.")

# Usage example
if __name__ == "__main__":
 analyzer = SentimentAnalyzer()
 analyzer.process_news_sentiment('ethereum')