import os
import logging
import yfinance as pandas_ta_alias # Solo referencia base
import yfinance as yf
import pandas as pd

logger = logging.getLogger(__name__)

class DataFetcher:
    def get_stock_data(self, ticker: str, period: str = "60d"):
        """Obtiene datos históricos de precios para análisis técnico."""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            if df.empty:
                logger.warning(f"No se encontraron datos históricos para {ticker}")
                return None
            return df
        except Exception as e:
            logger.error(f"Error obteniendo datos históricos de {ticker}: {str(e)}")
            return None

    def get_fundamental_data(self, ticker: str):
        """Obtiene información fundamental básica de la empresa."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "trailingPE": info.get("trailingPE"),
                "forwardPE": info.get("forwardPE"),
                "dividendYield": info.get("dividendYield"),
                "returnOnEquity": info.get("returnOnEquity"),
                "debtToEquity": info.get("debtToEquity"),
                "freeCashflow": info.get("freeCashflow"),
                "marketCap": info.get("marketCap")
            }
        except Exception as e:
            logger.error(f"Error obteniendo fundamentales de {ticker}: {str(e)}")
            return {}

    def get_analyst_ratings(self, ticker: str):
        """Obtiene recomendaciones de analistas."""
        try:
            stock = yf.Ticker(ticker)
            recommendations = stock.recommendations
            if recommendations is not None and not recommendations.empty:
                latest = recommendations.iloc[-1]
                return {
                    "strongBuy": latest.get("strongBuy", 0),
                    "buy": latest.get("buy", 0),
                    "hold": latest.get("hold", 0),
                    "sell": latest.get("sell", 0)
                }
            return {}
        except Exception as e:
            logger.error(f"Error obteniendo recomendaciones para {ticker}: {str(e)}")
            return {}

    def get_recent_news(self, ticker: str, days: int = 7):
        """Obtiene noticias recientes asociadas al ticker."""
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            if not news:
                return []
            return [{"title": item.get("title", ""), "publisher": item.get("publisher", "")} for item in news[:5]]
        except Exception as e:
            logger.error(f"Error obteniendo noticias para {ticker}: {str(e)}")
            return []

    def check_liquidity(self, ticker: str) -> float:
        """Verifica la liquidez basada en el volumen promedio."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            avg_volume = info.get("averageVolume", 0)
            market_cap = info.get("marketCap", 0)
            
            # Puntuación simple de liquidez (0 a 100)
            if avg_volume > 1000000 and market_cap > 2000000000:
                return 100.0
            elif avg_volume > 500000:
                return 70.0
            return 40.0
        except Exception as e:
            logger.error(f"Error evaluando liquidez de {ticker}: {str(e)}")
            return 50.0
              
