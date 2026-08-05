# =====================================
# CONFIGURACIÓN DEL BOT S&P 500
# Variables de entorno importadas de GitHub Actions
# =====================================

import os

# =====================================
# APIs y Tokens (desde variables de entorno)
# =====================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

# =====================================
# CONFIGURACIÓN DE SCORING
# =====================================

# Umbral mínimo de confianza para enviar alerta
CONFIDENCE_THRESHOLD = 80  # Solo alertas con puntaje >= 80

# Máximo de alertas por análisis
MAX_ALERTS_PER_RUN = 5

# =====================================
# HORARIO DE EJECUCIÓN
# =====================================

# Zona horaria de la bolsa USA
MARKET_TIMEZONE = "US/Eastern"

# Hora de apertura y cierre (formato 24h)
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 30
MARKET_CLOSE_HOUR = 16
MARKET_CLOSE_MINUTE = 0

# =====================================
# ANÁLISIS TÉCNICO - PERÍODOS
# =====================================

RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD_DEV = 2
MA_FAST = 50
MA_SLOW = 200
ADX_PERIOD = 14
STOCH_PERIOD = 14
STOCH_K = 3
STOCH_D = 3
ATR_PERIOD = 14

# Período de datos históricos para análisis técnico (días)
TECHNICAL_DATA_PERIOD = 60  # últimos 60 días

# =====================================
# ANÁLISIS FUNDAMENTAL - UMBRALES
# =====================================

MIN_ROE = 15  # % mínimo de ROE para considerar positivo
MAX_DEBT_TO_EQUITY = 1.0  # Máximo endeudamiento aceptable
MIN_LIQUIDITY_SCORE = 30  # Score mínimo de liquidez
MIN_MARKET_CAP = 1_000_000_000  # $1 billón mínimo

# =====================================
# ANÁLISIS MACRO - PALABRAS CLAVE
# =====================================

NEGATIVE_KEYWORDS = [
    "fraud",
    "scandal",
    "bankruptcy",
    "collapse",
    "crisis",
    "fine",
    "investigation",
    "lawsuit",
    "recall",
    "death",
]

POSITIVE_KEYWORDS = [
    "buyback",
    "acquisition",
    "partnership",
    "expansion",
    "record",
    "upgrade",
]

FED_KEYWORDS = ["federal reserve", "interest rate", "fed", "monetary policy"]
GEOPOLITICAL_KEYWORDS = ["war", "sanctions", "tariff", "trade", "conflict"]

# =====================================
# ALMACENAMIENTO Y ARCHIVOS
# =====================================

HISTORY_FILE = "data/alerts_history.json"
LAST_RUN_FILE = "data/last_run.json"
SP500_LIST_FILE = "data/sp500_list.csv"

# Días de historial a mantener
HISTORY_DAYS = 30

# =====================================
# SCORING - PESOS (PUNTOS POR SECCIÓN)
# =====================================

TECHNICAL_WEIGHT = 30  # Máximo 30 puntos
FUNDAMENTAL_WEIGHT = 40  # Máximo 40 puntos
MACRO_WEIGHT = 20  # Máximo 20 puntos

# Descuentos por riesgos
LIQUIDITY_RISK_DISCOUNT = 20
NEGATIVE_NEWS_DISCOUNT = 30
LEGAL_ISSUES_DISCOUNT = 40
BANKRUPTCY_RISK_DISCOUNT = 50
