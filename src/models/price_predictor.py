import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sqlalchemy import create_engine

class PricePredictor:
 def __init__(self, db_path='sqlite:///data/crypto_data.db'):
     self.engine = create_engine(db_path)
     self.scaler = MinMaxScaler()
     self.model = None

 def load_data(self, coin_id):
     query = f"SELECT * FROM {coin_id}_data"
     return pd.read_sql(query, self.engine)

 def prepare_data(self, df, lookback=30):
     features = ['price', 'volatility', 'avg_sentiment']
     scaled_data = self.scaler.fit_transform(df[features])
     
     X, y = [], []
     for i in range(lookback, len(scaled_data)):
         X.append(scaled_data[i-lookback:i])
         y.append(scaled_data[i, 0])  # Predicting the price
     
     return np.array(X), np.array(y)

 def build_model(self, input_shape):
     model = Sequential([
         LSTM(50, return_sequences=True, input_shape=input_shape),
         Dropout(0.2),
         LSTM(50, return_sequences=False),
         Dropout(0.2),
         Dense(1)
     ])
     model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
     return model

 def train_model(self, coin_id, epochs=100, batch_size=32, lookback=30):
     df = self.load_data(coin_id)
     X, y = self.prepare_data(df, lookback)
     
     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
     
     self.model = self.build_model((lookback, X.shape[2]))
     self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=1)
     
     return self.model

 def predict_next_day(self, coin_id):
     df = self.load_data(coin_id)
     features = ['price', 'volatility', 'avg_sentiment']
     last_30_days = df[features].tail(30).values
     scaled_data = self.scaler.transform(last_30_days)
     X = np.array([scaled_data])
     
     predicted_scaled = self.model.predict(X)
     predicted_price = self.scaler.inverse_transform(np.hstack([predicted_scaled, np.zeros((1, 2))]))[0, 0]
     
     return predicted_price

# Usage example
if __name__ == "__main__":
 predictor = PricePredictor()
 predictor.train_model('ethereum')
 next_day_price = predictor.predict_next_day('ethereum')
 print(f"Predicted price for tomorrow: ${next_day_price:.2f}")