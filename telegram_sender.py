import os
import requests
import logging

logger = logging.getLogger(__name__)

class TelegramSender:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN", "")

    def send_alert_message(self, chat_id: str, company_name: str, ticker: str, current_price: float, score_data: dict, technical_data: dict):
        if not self.token or not chat_id:
            logger.warning("Token o Chat ID de Telegram no configurados. Omitiendo envío.")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        
        message = (
            f"🚨 **OPORTUNIDAD DETECTADA EN S&P 500** 🚨\n\n"
            f"🏢 **Empresa:** {company_name} ({ticker})\n"
            f"💲 **Precio Actual:** ${current_price:.2f}\n"
            f"📊 **Puntaje Final:** {score_data.get('final_score')}/100\n"
            f"📈 **Tendencia:** {technical_data.get('trend')}\n"
            f"📉 **RSI:** {technical_data.get('rsi', 0):.1f}\n"
        )

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                logger.error(f"Error enviando mensaje a Telegram: {response.text}")
        except Exception as e:
            logger.error(f"Excepción al enviar alerta a Telegram: {str(e)}")
          
