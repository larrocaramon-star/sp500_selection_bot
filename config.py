# =====================================
# CONFIGURACIÓN DEL BOT S&P 500
# =====================================

# APIs y Tokens (IMPORTANTE: Se cargarán desde variables de entorno en GitHub)
TELEGRAM_BOT_TOKEN = "TU_TOKEN_AQUI"  # Se reemplazará en GitHub Actions
FINNHUB_API_KEY = "TU_FINNHUB_KEY_AQUI"  # Se reemplazará en GitHub Actions
NEWSAPI_KEY = "TU_NEWSAPI_KEY_AQUI"  # Se reemplazará en GitHub Actions

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
# ANÁLISIS TÉCNICO
# =====================================

# Períodos para indicadores técnicos
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
ATR_PERIOD = 14

# =====================================
# ANÁLISIS FUNDAMENTAL
# =====================================

# Umbrales para evaluar fundamentales
MIN_ROE = 15  # % mínimo de ROE para considerar positivo
MAX_DEBT_TO_EQUITY = 1.0  # Máximo endeudamiento aceptable
MIN_LIQUIDITY_SCORE = 30  # Score mínimo de liquidez

# =====================================
# HISTORIAL Y ALMACENAMIENTO
# =====================================

# Archivo de historial de alertas
HISTORY_FILE = "data/alerts_history.json"
LAST_RUN_FILE = "data/last_run.json"
SP500_LIST_FILE = "data/sp500_list.csv"

# Días de historial a mantener
HISTORY_DAYS = 30
