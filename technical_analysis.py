import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_all_indicators(self):
        try:
            close = self.df['Close']
            
            # Medias móviles
            sma_20 = close.rolling(window=20).mean()
            sma_50 = close.rolling(window=50).mean()
            
            # RSI (14)
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            current_price = float(close.iloc[-1])
            current_rsi = float(rsi.iloc[-1]) if not rsi.empty else 50.0
            curr_sma_20 = float(sma_20.iloc[-1]) if not sma_20.empty else current_price
            curr_sma_50 = float(sma_50.iloc[-1]) if not sma_50.empty else current_price

            # Tendencia simple
            trend = "BULLISH" if current_price > curr_sma_20 > curr_sma_50 else "NEUTRAL"

            return {
                "current_price": current_price,
                "rsi": current_rsi,
                "sma_20": curr_sma_20,
                "sma_50": curr_sma_50,
                "trend": trend
            }
        except Exception as e:
            return None
          
