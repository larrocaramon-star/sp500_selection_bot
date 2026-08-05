# =====================================
# SCORING MODULE - SISTEMA DE PUNTUACIÓN (0-100)
# =====================================
# Agrupa técnico, fundamental, macro y aplica descuentos por riesgos.

import logging
from config import (
    CONFIDENCE_THRESHOLD,
    LIQUIDITY_RISK_DISCOUNT,
    NEGATIVE_NEWS_DISCOUNT,
    LEGAL_ISSUES_DISCOUNT,
    BANKRUPTCY_RISK_DISCOUNT,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScoringEngine:
    """
    Motor encargado de calcular el puntaje final de confianza (0-100).
    """
    def __init__(self, technical_result, fundamental_result, macro_result, liquidity_score):
        self.tech = technical_result or {}
        self.fund = fundamental_result or {}
        self.macro = macro_result or {}
        self.liquidity = liquidity_score or 0

    def calculate_final_score(self):
        """
        Calcula el puntaje final aplicando exclusiones, pesos y descuentos.
        """
        try:
            # 1. Comprobar exclusiones automáticas
            # Si no pasa los filtros fundamentales básicos, se descarta de inmediato
            if not self.fund.get("passed_filters", True):
                logger.info("Empresa rechazada por filtros fundamentales automáticos.")
                return {"final_score": 0, "included": False, "reason": "Filtros fundamentales no superados"}

            # Verificar volumen o liquidez baja extrema
            if self.liquidity < 30:
                logger.info("Empresa rechazada por baja liquidez.")
                return {"final_score": 0, "included": False, "reason": "Liquidez baja (<30)"}

            # Verificar riesgos críticos detectados en macro/noticias
            if self.macro.get("bankruptcy_risk", False):
                return {"final_score": 0, "included": False, "reason": "Riesgo de quiebra detectado"}

            # 2. Calcular puntajes parciales
            # Técnico: hasta 30 puntos (basado en cuántos de los 10 indicadores se cumplen, ej: 3 puntos c/u)
            tech_signals = self.tech.get("positive_signals_count", 0)
            tech_score = min(30, tech_signals * 3)

            # Fundamental: hasta 40 puntos
            fund_score = self.fund.get("score", 0)

            # Macro: hasta 20 puntos
            macro_score = self.macro.get("score", 0)

            raw_score = tech_score + fund_score + macro_score

            # 3. Aplicar descuentos por riesgos
            discounts = 0
            risk_reasons = []

            if self.liquidity < 50:
                discounts += LIQUIDITY_RISK_DISCOUNT
                risk_reasons.append("Liquidez moderadamente baja")

            if self.macro.get("has_very_negative_news", False):
                discounts += NEGATIVE_NEWS_DISCOUNT
                risk_reasons.append("Noticias muy negativas recientes")

            if self.macro.get("has_legal_issues", False):
                discounts += LEGAL_ISSUES_DISCOUNT
                risk_reasons.append("Problemas legales o investigaciones")

            final_score = max(0, raw_score - discounts)

            # 4. Comprobar umbral de confianza (Umbral 80 acordado)
            included = final_score >= CONFIDENCE_THRESHOLD

            return {
                "final_score": final_score,
                "tech_score": tech_score,
                "fund_score": fund_score,
                "macro_score": macro_score,
                "discounts_applied": discounts,
                "risk_reasons": risk_reasons,
                "included": included,
                "active_signals": self.tech.get("active_signals_list", []),
                "fundamental_details": self.fund.get("details", []),
                "macro_details": self.macro.get("details", [])
            }

        except Exception as e:
            logger.error(f"Error calculando scoring final: {str(e)}")
            return {"final_score": 0, "included": False, "reason": f"Error interno: {str(e)}"}
          
