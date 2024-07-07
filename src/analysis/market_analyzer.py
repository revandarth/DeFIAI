import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

class MarketAnalyzer:
 def __init__(self, db_path='sqlite:///data/crypto_data.db'):
     self.engine = create_engine(db_path)

 def load_data(self, coin_id):
     query = f"SELECT * FROM {coin_id}_data"
     return pd.read_sql(query, self.engine)

 def calculate_correlations(self, df):
     corr = df[['returns', 'volatility', 'avg_sentiment']].corr()
     return corr

 def granger_causality_test(self, df, variables):
     results = {}
     for v1 in variables:
         for v2 in variables:
             if v1 != v2:
                 test_result = sm.tsa.stattools.grangercausalitytests(df[[v1, v2]], maxlag=5, verbose=False)
                 min_p_value = min([test_result[i+1][0]['ssr_ftest'][1] for i in range(5)])
                 results[f"{v1} → {v2}"] = min_p_value
     return pd.DataFrame(results, index=['p-value']).T

 def plot_time_series(self, df, coin_id):
     fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15), sharex=True)
     
     ax1.plot(df['date'], df['price'])
     ax1.set_title(f'{coin_id.capitalize()} Price')
     ax1.set_ylabel('Price (USD)')

     ax2.plot(df['date'], df['volatility'])
     ax2.set_title('Volatility')
     ax2.set_ylabel('Volatility')

     ax3.plot(df['date'], df['avg_sentiment'])
     ax3.set_title('Average Sentiment')
     ax3.set_ylabel('Sentiment Score')

     plt.tight_layout()
     plt.savefig(f'data/{coin_id}_time_series.png')
     plt.close()

 def analyze_market(self, coin_id):
     df = self.load_data(coin_id)
     
     correlations = self.calculate_correlations(df)
     print("Correlations:")
     print(correlations)

     granger_results = self.granger_causality_test(df, ['returns', 'volatility', 'avg_sentiment'])
     print("\nGranger Causality Test Results:")
     print(granger_results)

     self.plot_time_series(df, coin_id)
     print(f"Time series plot saved as data/{coin_id}_time_series.png")

     return {
         'correlations': correlations,
         'granger_causality': granger_results,
         'data': df
     }

# Usage example
if __name__ == "__main__":
 analyzer = MarketAnalyzer()
 results = analyzer.analyze_market('ethereum')