class ScoringEngine:
    def __init__(self, tech_result: dict, fund_result: dict, macro_result: dict, liquidity_score: float):
        self.tech_result = tech_result
        self.fund_result = fund_result
        self.macro_result = macro_result
        self.liquidity_score = liquidity_score

    def calculate_final_score(self):
        # 1. PUNTUACIÓN TÉCNICA DINÁMICA (En lugar de un 80 fijo si es BULLISH)
        trend = self.tech_result.get("trend", "NEUTRAL")
        rsi = self.tech_result.get("rsi", 50.0)
        current_price = self.tech_result.get("current_price", 0)
        sma_20 = self.tech_result.get("sma_20", current_price)

        tech_score = 50.0
        if trend == "BULLISH":
            tech_score += 20.0
            
        # Bonificación o penalización fina según el RSI (ej: RSI saludable entre 45 y 65 suma más)
        if 45.0 <= rsi <= 65.0:
            tech_score += 15.0
        elif rsi > 75.0:
            tech_score -= 10.0 # Sobrecomprado, baja un poco
        elif rsi < 35.0:
            tech_score += 10.0 # Posible rebote por sobreventa

        # Bonificación si el precio está por encima de la media de 20
        if current_price > sma_20:
            tech_score += 15.0

        tech_score = max(0.0, min(100.0, tech_score))

        # 2. OTROS COMPONENTES
        fund_score = self.fund_result.get("fundamental_score", 50.0)
        macro_score = self.macro_result.get("macro_score", 50.0)

        # 3. PONDERACIÓN FINAL EQUILIBRADA
        final_score = (
            (tech_score * 0.45) + 
            (fund_score * 0.30) + 
            (macro_score * 0.15) + 
            (self.liquidity_score * 0.10)
        )
        
        # Umbral estricto para que solo pasen las mejores y con puntajes diversos
        included = final_score >= 65.0

        return {
            "final_score": round(final_score, 2),
            "included": included
        }
        
