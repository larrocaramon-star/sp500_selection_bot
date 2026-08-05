# =====================================
# FUNDAMENTAL ANALYSIS - ANÁLISIS FUNDAMENTAL
# =====================================
# Evalúa la salud financiera de la empresa (P/E, ROE, Deuda, etc.)

import logging
from config import (
    MIN_ROE,
    MAX_DEBT_TO_EQUITY,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FundamentalAnalyzer:
    """
    Clase para analizar los datos fundamentales de una empresa.
    """
    def __init__(self, fundamental_data, analyst_ratings):
        """
        Recibe los datos fundamentales y las calificaciones de analistas.
        """
        self.fund = fundamental_data or {}
        self.ratings = analyst_ratings or {}

    def evaluate_fundamentals(self):
        """
        Evalúa los criterios fundamentales y otorga puntos (hasta 40 puntos máximo).
        Retorna un diccionario con el puntaje y los detalles.
        """
        try:
            if not self.fund:
                logger.warning("No hay datos fundamentales para evaluar.")
                return {"score": 0, "details": [], "passed_filters": False}

            score = 0
            details = []

            # 1. Ratio P/E (Precio / Beneficio) bajo o razonable
            pe_ratio = self.fund.get("pe_ratio")
            if pe_ratio is not None and 0 < pe_ratio < 25:
                score += 10
                details.append(f"P/E favorable ({pe_ratio:.1f})")

            # 2. ROE (Return on Equity) alto (> 15%)
            roe = self.fund.get("roe")
            if roe is not None and roe >= MIN_ROE:
                score += 10
                details.append(f"ROE sólido ({roe:.1f}%)")

            # 3. Deuda manejable (Debt to Equity < 1.0)
            debt_to_equity = self.fund.get("debt_to_equity")
            if debt_to_equity is not None and debt_to_equity <= MAX_DEBT_TO_EQUITY:
                score += 10
                details.append(f"Deuda controlada (Debt/Equity: {debt_to_equity:.2f})")

            # 4. Calificaciones de analistas positivas (Buy / Strong Buy predominante)
            strong_buys = self.ratings.get("strong_buy_count", 0)
            buys = self.ratings.get("buy_count", 0)
            if (strong_buys + buys) > 5:
                score += 10
                details.append(f"Consenso de analistas positivo ({strong_buys + buys} compras)")

            # Exclusiones automáticas por fundamentales deficientes
            earnings_are_negative = pe_ratio is not None and pe_ratio < 0
            excessive_debt = debt_to_equity is not None and debt_to_equity > 3.0

            passed_filters = True
            if earnings_are_negative or excessive_debt:
                passed_filters = False
                logger.warning(f"Empresa descartada por fundamentales críticos. P/E negativo o deuda excesiva.")

            return {
                "score": min(40, score), # Máximo 40 puntos
                "details": details,
                "passed_filters": passed_filters,
                _eval_earnings_negative: earnings_are_negative,
                _eval_excessive_debt: excessive_debt
            }

        except Exception as e:
            logger.error(f"Error evaluando fundamentales: {str(e)}")
            return {"score": 0, "details": [], "passed_filters": False}
          
