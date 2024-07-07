import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from sqlalchemy import create_engine
from src.analysis.market_analyzer import MarketAnalyzer
from src.models.price_predictor import PricePredictor
from src.blockchain.contract_interactor import ContractInteractor

class Dashboard:
 def __init__(self):
     self.engine = create_engine('sqlite:///data/crypto_data.db')
     self.market_analyzer = MarketAnalyzer()
     self.price_predictor = PricePredictor()
     self.contract_interactor = ContractInteractor()

 def load_data(self, coin_id):
     return pd.read_sql(f"SELECT * FROM {coin_id}_data", self.engine)

 def plot_price_chart(self, df):
     fig = go.Figure()
     fig.add_trace(go.Scatter(x=df['date'], y=df['price'], name='Price'))
     fig.update_layout(title='Price Chart', xaxis_title='Date', yaxis_title='Price (USD)')
     st.plotly_chart(fig)

 def plot_sentiment_chart(self, df):
     fig = go.Figure()
     fig.add_trace(go.Scatter(x=df['date'], y=df['avg_sentiment'], name='Sentiment'))
     fig.update_layout(title='Sentiment Chart', xaxis_title='Date', yaxis_title='Sentiment Score')
     st.plotly_chart(fig)

 def display_correlations(self, coin_id):
     correlations = self.market_analyzer.calculate_correlations(self.load_data(coin_id))
     st.write("Correlations:")
     st.write(correlations)

 def display_price_prediction(self, coin_id):
     predicted_price = self.price_predictor.predict_next_day(coin_id)
     st.write(f"Predicted price for tomorrow: ${predicted_price:.2f}")

 def display_contract_info(self):
     latest_price = self.contract_interactor.get_latest_price()
     st.write(f"Latest price from smart contract: ${latest_price:.2f}")

 def run(self):
     st.title('CryptoDEX Insights AI Dashboard')

     coin_id = st.selectbox('Select Cryptocurrency', ['ethereum', 'bitcoin'])

     df = self.load_data(coin_id)

     self.plot_price_chart(df)
     self.plot_sentiment_chart(df)
     self.display_correlations(coin_id)
     self.display_price_prediction(coin_id)
     self.display_contract_info()

     if st.button('Request New Price Prediction'):
         self.contract_interactor.request_prediction()
         st.success('New price prediction requested!')

if __name__ == "__main__":
 dashboard = Dashboard()
 dashboard.run()