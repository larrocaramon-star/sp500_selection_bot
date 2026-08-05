# =====================================
# MACRO ANALYSIS - ANÁLISIS MACRO Y NOTICIAS
# =====================================
# Analiza noticias, eventos geopolíticos y riesgos en los textos recientes.

import logging
from config import (
    NEGATIVE_KEYWORDS,
    POSITIVE_KEYWORDS,
    FED_KEYWORDS,
    GEOPOLITICAL_KEYWORDS,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MacroAnalyzer:
    """
    Clase para evaluar el entorno macroeconómico y noticias de la empresa.
    """
    def __init__(self, news_articles):
        """
        Recibe una lista de artículos de noticias recientes.
        """
        self.articles = news_articles or []

    def evaluate_macro_and_news(self):
        """
        Analiza las noticias buscando palabras clave positivas y negativas.
        Otorga hasta 20 puntos y detecta riesgos graves (descuentos o exclusiones).
        """
        try:
            score = 10  # Base neutra en macro
            details = []
            has_legal_issues = False
            has_very_negative_news = False
            bankruptcy_risk = False

            negative_count = 0
            positive_count = 0

            for article in self.articles:
                title = article.get("title", "").lower()
                description = article.get("description", "").lower()
                full_text = f"{title} {description}"

                # Buscar palabras clave negativas graves
                for word in NEGATIVE_KEYWORDS:
                    if word in full_text:
                        negative_count += 1
                        if word in ["fraud", "scandal", "investigation", "lawsuit"]:
                            has_legal_issues = True
                        if word in ["bankruptcy", "collapse"]:
                            bankruptcy_risk = True
                        if word in ["crisis", "recall", "death"]:
                            has_very_negative_news = True

                # Buscar palabras clave positivas
                for word in POSITIVE_KEYWORDS:
                    if word in full_text:
                        positive_count += 1

                # Buscar menciones macro o geopolíticas
                for word in FED_KEYWORDS + GEOPOLITICAL_KEYWORDS:
                    if word in full_text:
                        details.append(f"Mención macro relevante: {word}")

            # Ajustar puntaje según el balance de noticias
            if positive_count > negative_count:
                score += 10
                details.append("Noticias recientes con tinte expansivo/positivo")
            elif negative_count > positive_count:
                score -= 10
                details.append("Presencia de noticias adversas recientes")

            # Limitar el score macro entre 0 y 20
            final_macro_score = max(0, min(20, score))

            return {
                "score": final_macro_score,
                "details": details,
                "has_legal_issues": has_legal_issues,
                "has_very_negative_news": has_very_negative_news,
                "bankruptcy_risk": bankruptcy_risk
            }

        except Exception as e:
            logger.error(f"Error en análisis macro/noticias: {str(e)}")
            return {
                "score": 10,
                "details": [],
                "has_legal_issues": False,
                "has_very_negative_news": False,
                "bankruptcy_risk": False
      }
          
