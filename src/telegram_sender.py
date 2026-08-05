# =====================================
# TELEGRAM SENDER - ENVÍO DE ALERTAS
# =====================================
# Formatea y envía las alertas de oportunidades al bot de Telegram.

import requests
import logging
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramSender:
    """
    Clase para enviar mensajes formateados a través de Telegram Bot API.
    """
    def __init__(self, bot_token=None):
        self.token = bot_token or TELEGRAM_BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_alert_message(self, chat_id, company_name, ticker, current_price, score_data, technical_data):
        """
        Formatea el mensaje de alerta de compra y lo envía por Telegram.
        """
        try:
            if not self.token or not chat_id:
                logger.warning("Token de Telegram o Chat ID no configurados.")
                return False

            # Calcular datos adicionales para el formato
            prev_price = technical_data.get("prev_price", current_price)
            price_change_pct = ((current_price - prev_price) / prev_price) * 100
            bb_high = technical_data.get("bb_high", current_price * 1.1)

            # Construir viñetas de indicadores positivos
            signals_text = ""
            for sig in score_data.get("active_signals", []):
                signals_text += f"✓ {sig}\n"
            if not signals_text:
                signals_text = "✓ Indicadores técnicos favorables en conjunto\n"

            # Construir riesgos si los hay
            risks_text = ""
            for risk in score_data.get("risk_reasons", []):
                risks_text += f"⚠️ {risk}\n"
            if not risks_text:
                risks_text = "✓ Sin riesgos críticos aparentes\n"

            # Fecha actual formateada
            current_date_str = datetime.now().strftime("%d-%m-%Y %H:%M ET")

            # Armar mensaje con el diseño acordado
            message = (
                f"🎯 **OPORTUNIDAD DE COMPRA**\n"
                f"Empresa: **{company_name.upper()}**\n"
                f"Ticker: `{ticker}`\n"
                f"Precio Actual: `${current_price:.2f}`\n"
                f"Máximo reciente (BB High): `${bb_high:.2f}`\n"
                f"Variación reciente: `{price_change_pct:+.1f}%`\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"**PUNTAJE DE CONFIANZA: {score_data.get('final_score', 0)}/100 ✅**\n\n"
                f"**RESUMEN:**\n"
                f"Acción analizada bajo rigurosos filtros de calidad. Fundamentales sólidos y "
                f"soporte técnico detectado para horizonte de mediano plazo.\n\n"
                f"**INDICADORES POSITIVOS:**\n"
                f"{signals_text}\n"
                f"**RIESGOS Y ADVERTENCIAS:**\n"
                f"{risks_text}\n"
                f"**HORIZONTE:** 1-2 meses\n"
                f"**RECOMENDACIÓN:** Acumulación en soportes\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Análisis: {current_date_str}"
            )

            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }

            response = requests.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Alerta enviada exitosamente para {ticker}")
            return True

        except Exception as e:
            logger.error(f"Error enviando mensaje a Telegram: {str(e)}")
            return False
          
