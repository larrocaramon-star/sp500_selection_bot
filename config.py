import os

# Configuración general del Bot S&P 500
SP500_LIST_FILE = os.getenv("SP500_LIST_FILE", "data/sp500_list.csv")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "60.0"))
MAX_ALERTS_PER_RUN = int(os.getenv("MAX_ALERTS_PER_RUN", "5"))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
