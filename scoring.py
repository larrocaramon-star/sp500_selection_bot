class ScoringEngine:
    def __init__(self, tech_result: dict, fund_result: dict, macro_result: dict, liquidity_score: float):
        self.tech_result = tech_result
        self.fund_result = fund_result
        self.macro_result = macro_result
        self.liquidity_score = liquidity_score

    def calculate_final_score(self):
        # Ponderaciones equilibradas (Técnico y Fundamental dominan, Macro/Noticias influye levemente)
        tech_score = 80.0 if self.tech_result.get("trend") == "BULLISH" else 50.0
        fund_score = self.fund_result.get("fundamental_score", 50.0)
        macro_score = self.macro_result.get("macro_score", 50.0)

        # Pesos: Técnico 45%, Fundamental 35%, Macro/Noticias 10%, Liquidez 10%
        final_score = (
            (tech_score * 0.45) + 
            (fund_score * 0.35) + 
            (macro_score * 0.10) + 
            (self.liquidity_score * 0.10)
        )
        
        # Umbral para incluir la oportunidad
        included = final_score >= 60.0

        return {
            "final_score": round(final_score, 2),
            "included": included
        }
        
