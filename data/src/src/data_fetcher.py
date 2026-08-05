# =====================================
# DATA FETCHER - OBTIENE DATOS DE APIs
# =====================================
# Este archivo descarga datos de:
# - yfinance: Datos técnicos e históricos
# - Finnhub: Datos fundamentales
# - NewsAPI: Noticias recientes

import yfinance as yf
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
import logging

# Importar configuración
from config import (
    FINNHUB_API_KEY,
    NEWSAPI_KEY,
    TECHNICAL_DATA_PERIOD,
    MIN_MARKET_CAP,
)

# Configurar logging (para ver mensajes de error)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """
    Clase que se encarga de obtener datos de todas las APIs.
    
    ¿Qué es una clase?
    Una clase es como un "contenedor" de funciones relacionadas.
    Agrupa todo lo que necesita un fetcher de datos en un lugar.
    """
    
    def __init__(self):
        """
        Constructor - Se ejecuta cuando creamos una instancia de DataFetcher
        Aquí inicializamos las variables que usaremos en toda la clase
        """
        self.finnhub_url = "https://finnhub.io/api/v1"
        self.newsapi_url = "https://newsapi.org/v2"
        self.request_delay = 0.1  # Delay entre requests para no sobrecargar APIs
    
    def get_stock_data(self, ticker, period="60d"):
        """
        Obtiene datos históricos de precio y volumen de yfinance
        
        Parámetros:
        - ticker: código de la empresa (ej: "AAPL")
        - period: período histórico (ej: "60d" = 60 días)
        
        Retorna:
        - DataFrame de pandas con datos OHLCV (Open, High, Low, Close, Volume)
        """
        try:
            logger.info(f"Obteniendo datos técnicos para {ticker}...")
            
            # Descargar datos históricos
            data = yf.download(
                ticker,
                period=period,
                progress=False,  # No mostrar barra de progreso
                interval="1d"  # Datos diarios
            )
            
            if data.empty:
                logger.warning(f"No hay datos para {ticker}")
                return None
            
            return data
        
        except Exception as e:
            logger.error(f"Error al obtener datos de {ticker}: {str(e)}")
            return None
    
    def get_fundamental_data(self, ticker):
        """
        Obtiene datos fundamentales usando Finnhub API
        
        Parámetros:
        - ticker: código de la empresa
        
        Retorna:
        - Diccionario con: P/E, ROE, deuda, capitalización, etc.
        """
        try:
            time.sleep(self.request_delay)  # Esperar para no sobrecargar
            
            logger.info(f"Obteniendo datos fundamentales para {ticker}...")
            
            # Endpoint: Finn Hub Profile
            url = f"{self.finnhub_url}/stock/profile2"
            params = {
                "symbol": ticker,
                "token": FINNHUB_API_KEY
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()  # Lanzar error si hay problema
            
            profile = response.json()
            
            if not profile:
                logger.warning(f"No hay perfil para {ticker}")
                return None
            
            # Extraer datos importantes
            fundamental_data = {
                "ticker": ticker,
                "company_name": profile.get("name", "N/A"),
                "market_cap": profile.get("marketCap", 0),
                "industry": profile.get("finnhubIndustry", "N/A"),
                "website": profile.get("weburl", "N/A"),
                "country": profile.get("country", "N/A"),
            }
            
            # Obtener métricas de valuación (P/E, P/B, etc)
            fundamental_data.update(self._get_valuation_metrics(ticker))
            
            # Obtener información de dividendos
            fundamental_data.update(self._get_dividend_info(ticker))
            
            return fundamental_data
        
        except Exception as e:
            logger.error(f"Error al obtener fundamentales de {ticker}: {str(e)}")
            return None
    
    def _get_valuation_metrics(self, ticker):
        """
        Obtiene métricas de valuación (P/E, ROE, etc) desde Finnhub
        """
        try:
            time.sleep(self.request_delay)
            
            url = f"{self.finnhub_url}/stock/metric"
            params = {
                "symbol": ticker,
                "metric": "all",
                "token": FINNHUB_API_KEY
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            metrics = response.json()
            metric_data = metrics.get("metric", {})
            
            return {
                "pe_ratio": metric_data.get("peRatio", None),
                "roe": metric_data.get("roe", None),
                "debt_to_equity": metric_data.get("debtToEquity", None),
                "current_ratio": metric_data.get("currentRatio", None),
                "quick_ratio": metric_data.get("quickRatio", None),
                "revenue_growth": metric_data.get("revenuePerShare", None),
            }
        
        except Exception as e:
            logger.error(f"Error al obtener métricas de {ticker}: {str(e)}")
            return {}
    
    def _get_dividend_info(self, ticker):
        """
        Obtiene información de dividendos
        """
        try:
            # Usar yfinance para información de dividendos
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                "dividend_yield": info.get("dividendYield", 0),
                "payout_ratio": info.get("payoutRatio", 0),
            }
        
        except Exception as e:
            logger.error(f"Error al obtener dividendos de {ticker}: {str(e)}")
            return {}
    
    def get_analyst_ratings(self, ticker):
        """
        Obtiene calificaciones de analistas desde Finnhub
        
        Retorna:
        - Diccionario con recomendaciones de analistas (Buy, Hold, Sell)
        """
        try:
            time.sleep(self.request_delay)
            
            logger.info(f"Obteniendo ratings de analistas para {ticker}...")
            
            url = f"{self.finnhub_url}/stock/recommendation"
            params = {
                "symbol": ticker,
                "token": FINNHUB_API_KEY
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            ratings = response.json()
            
            if not ratings:
                return None
            
            # Tomar la recomendación más reciente
            latest = ratings[0]
            
            return {
                "ticker": ticker,
                "buy_count": latest.get("buy", 0),
                "hold_count": latest.get("hold", 0),
                "sell_count": latest.get("sell", 0),
                "strong_buy_count": latest.get("strongBuy", 0),
                "strong_sell_count": latest.get("strongSell", 0),
            }
        
        except Exception as e:
            logger.error(f"Error al obtener ratings de {ticker}: {str(e)}")
            return None
    
    def get_recent_news(self, ticker, days=7):
        """
        Obtiene noticias recientes de NewsAPI
        
        Parámetros:
        - ticker: código de la empresa
        - days: cuántos días atrás buscar noticias
        
        Retorna:
        - Lista de noticias con título y descripción
        """
        try:
            time.sleep(self.request_delay)
            
            logger.info(f"Obteniendo noticias para {ticker}...")
            
            # Calcular fecha de inicio
            from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            url = f"{self.newsapi_url}/everything"
            params = {
                "q": ticker,  # Buscar por ticker
                "from": from_date,
                "sortBy": "publishedAt",  # Ordenar por fecha
                "language": "en",
                "apiKey": NEWSAPI_KEY
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            news_data = response.json()
            articles = news_data.get("articles", [])
            
            # Retornar solo los primeros 5 artículos más recien
