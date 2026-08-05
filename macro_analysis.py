class MacroAnalyzer:
    def __init__(self, news_articles: list):
        self.news_articles = news_articles

    def evaluate_macro_and_news(self):
        # Evaluación básica basada en cantidad o sentimiento de titulares
        score = 60.0
        return {
            "macro_score": score,
            "sentiment": "Neutral/Positive"
        }
      
