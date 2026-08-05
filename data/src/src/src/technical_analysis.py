# =====================================
# TECHNICAL ANALYSIS - INDICADORES TÉCNICOS
# =====================================
# Este archivo calcula los 10 indicadores técnicos clave:
# 1. RSI, 2. MACD, 3. Bandas de Bollinger, 4. MA50, 5. MA200
# 6. Volumen SMA, 7. ADX, 8. Stochastic, 9. ATR, 10. VWAP, 11. OBV

import pandas as pd
import numpy as np
import ta
import logging

from config import (
    RSI_PERIOD,
    MACD_FAST,
    MACD_SLOW,
    MACD_SIGNAL,
    BB_PERIOD,
    BB_STD_DEV,
    MA_FAST,
    MA_SLOW,
    ADX_PERIOD,
    STOCH_PERIOD,
    STOCH_K,
    STOCH_D,
    ATR_PERIOD,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """
    Clase encargada de calcular todos los indicadores técnicos.
    """
    def __init__(self, df):
        """
        Recibe un DataFrame con datos históricos (Open, High, Low, Close, Volume)
        """
        self.df = df.copy()
        self._prepare_data()

    def _prepare_data(self):
        """
        Limpia y asegura que los nombres de las columnas sean correctos
        """
        # A veces yfinance devuelve columnas multi-index, las aplanamos si es necesario
        if isinstance(self.df.columns, pd.MultiIndex):
            self.df.columns = self.df.columns.get_level_values(0)
        
        # Asegurar minúsculas o nombres estándar
        self.df.columns = [col.lower() for col in self.df.columns]

    def calculate_all_indicators(self):
        """
        Calcula los 10 indicadores técnicos definidos en la arquitectura.
        Retorna un diccionario con los valores actuales de cada indicador.
        """
        try:
            if self.df is None or len(self.df) < MA_SLOW:
                logger.warning("Datos insuficientes para calcular todos los indicadores.")
                return None

            close = self.df['close']
            high = self.df['high']
            low = self.df['low']
            volume = self.df['volume']

            # 1. RSI (Relative Strength Index)
            rsi_series = ta.momentum.RSIIndicator(close, window=RSI_PERIOD).rsi()
            current_rsi = rsi_series.iloc[-1]

            # 2. MACD (Moving Average Convergence Divergence)
            macd_indicator = ta.trend.MACD(
                close, 
                window_slow=MACD_SLOW, 
                window_fast=MACD_FAST, 
                window_sign=MACD_SIGNAL
            )
            current_macd = macd_indicator.macd().iloc[-1]
            current_macd_signal = macd_indicator.macd_signal().iloc[-1]
            current_macd_diff = macd_indicator.macd_diff().iloc[-1]

            # 3. Bandas de Bollinger
            bb_indicator = ta.volatility.BollingerBands(
                close, 
                window=BB_PERIOD, 
                window_dev=BB_STD_DEV
            )
            current_bb_high = bb_indicator.bollinger_hband().iloc[-1]
            current_bb_low = bb_indicator.bollinger_lband().iloc[-1]
            current_bb_mid = bb_indicator.bollinger_mavg().iloc[-1]

            # 4 y 5. Medias Móviles (MA50 y MA200)
            ma_fast_series = ta.trend.SMAIndicator(close, window=MA_FAST).sma_indicator()
            ma_slow_series = ta.trend.SMAIndicator(close, window=MA_SLOW).sma_indicator()
            current_ma_fast = ma_fast_series.iloc[-1]
            current_ma_slow = ma_slow_series.iloc[-1]

            # 6. Volumen SMA (Promedio de volumen a 20 ruedas)
            vol_sma = ta.trend.SMAIndicator(volume, window=20).sma_indicator()
            current_vol_sma = vol_sma.iloc[-1]
            current_volume = volume.iloc[-1]

            # 7. ADX (Average Directional Index - Fuerza de tendencia)
            adx_indicator = ta.trend.ADXIndicator(high, low, close, window=ADX_PERIOD)
            current_adx = adx_indicator.adx().iloc[-1]

            # 8. Stochastic Oscillator
            stoch = ta.momentum.StochasticOscillator(high, low, close, window=STOCH_PERIOD, smooth_window=STOCH_K)
            current_stoch_k = stoch.stoch().iloc[-1]
            current_stoch_d = stoch.stoch_signal().iloc[-1]

            # 9. ATR (Average True Range - Volatilidad)
            atr_indicator = ta.volatility.AverageTrueRange(high, low, close, window=ATR_PERIOD)
            current_atr = atr_indicator.average_true_range().iloc[-1]

            # 10. OBV (On-Balance Volume - Presión compradora/vendedora)
            obv_indicator = ta.volume.OnBalanceVolumeIndicator(close, volume)
            current_obv = obv_indicator.on_balance_volume().iloc[-1]
            previous_obv = obv_indicator.on_balance_volume().iloc[-2]

            # Precio actual de cierre
            current_price = close.iloc[-1]
            prev_price = close.iloc[-2]

            # Evaluar señales positivas individuales (para el sistema de scoring)
            positive_signals_count = 0
            active_signals_list = []

            # Condición RSI: Sobreventa (< 40) o rebote saludable
            if current_rsi < 40:
                positive_signals_count += 1
                active_signals_list.append(f"RSI en zona de sobreventa ({current_rsi:.1f})")

            # Condición Precio vs MA50
            if current_price > current_ma_fast:
                positive_signals_count += 1
                active_signals_list.append("Precio por encima de MA50")

            # Condición MACD: Cruce alcista (histograma positivo o en aumento)
            if current_macd_diff > 0:
                positive_signals_count += 1
                active_signals_list.append("MACD en territorio positivo / rebote")

            # Condición Bollinger: Cerca de banda inferior (oportunidad de rebote) o ruptura alcista
            if current_price <= current_bb_low * 1.02:
                positive_signals_count += 1
                active_signals_list.append("Precio apoyado en Banda de Bollinger Inferior")

            # Condición Tendencia ADX: Tendencia fuerte (> 25)
            if current_adx > 25:
                positive_signals_count += 1
                active_signals_list.append(f"ADX indica tendencia fuerte ({current_adx:.1f})")

            # Condición OBV creciente
            if current_obv > previous_obv:
                positive_signals_count += 1
                active_signals_list.append("OBV creciente (presión institucional compradora)")

            # Condición Stochastic en zona baja cruzándose al alza
            if current_stoch_k < 30 and current_stoch_k > current_stoch_d:
                positive_signals_count += 1
                active_signals_list.append("Stochastic cruzando al alza desde zona de sobreventa")

            # Consolidar resultados técnicos
            analysis_result = {
                "current_price": current_price,
                "prev_price": prev_price,
                "rsi": current_rsi,
                "macd": current_macd,
                "macd_signal": current_macd_signal,
                "bb_high": current_bb_high,
                "bb_low": current_bb_low,
                "ma_fast": current_ma_fast,
                "ma_slow": current_ma_slow,
                "adx": current_adx,
                "stoch_k": current_stoch_k,
                "atr": current_atr,
                "obv": current_obv,
                "volume": current_volume,
                "volume_sma": current_vol_sma,
                "positive_signals_count": min(10, positive_signals_count), # Tope de 10 indicadores
                "active_signals_list": active_signals_list
            }

            return analysis_result

        except Exception as e:
            logger.error(f"Error calculando indicadores técnicos: {str(e)}")
            return None
          
