class MacroAnalyzer:
    def __init__(self, news_articles: list):
        self.news_articles = news_articles

    def evaluate_macro_and_news(self):
        """Analiza titulares recientes buscando sentimiento de mercado y riesgo macro/geopolítico."""
        if not self.news_articles:
            return {
                "macro_score": 50.0,
                "sentiment": "Neutral (Sin noticias recientes)"
            }

        positive_keywords = ["growth", "record", "beat", "expansion", "bullish", "profit", "surge", "up", "sube", "crecimiento"]
        negative_keywords = ["fall", "drop", "inflation", "risk", "war", "conflict", "loss", "crash", "down", "baja", "crisis", "riesgo"]

        score = 50.0
        sentiment_count = 0

        for article in self.news_articles:
            title = article.get("title", "").lower()
            
            # Buscar palabras positivas
            if any(word in title for word in positive_keywords):
                score += 10.0
                sentiment_count += 1
                
            # Buscar palabras negativas o de riesgo macro/geopolítico
            if any(word in title for word in negative_keywords):
                score -= 10.0
                sentiment_count -= 1

        # Limitar el puntaje entre 0 y 100
        final_macro_score = max(0.0, min(100.0, score + 10.0)) # Base un poco optimista si hay noticias activas

        sentiment_label = "Neutral"
        if sentiment_count > 0:
            sentiment_label = "Positivo / Favorable"
        elif sentiment_count < 0:
            sentiment_label = "Precaución / Riesgo Macro"

        return {
            "macro_score": round(final_macro_score, 2),
            "sentiment": sentiment_label
        }
        
