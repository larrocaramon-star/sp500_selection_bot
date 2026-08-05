class FundamentalAnalyzer:
    def __init__(self, fund_data: dict, analyst_ratings: dict):
        self.fund_data = fund_data
        self.analyst_ratings = analyst_ratings

    def evaluate_fundamentals(self):
        score = 50.0
        pe = self.fund_data.get("trailingPE")
        roe = self.fund_data.get("returnOnEquity")

        if pe and 0 < pe < 25:
            score += 15.0
        if roe and roe > 0.15:
            score += 15.0

        return {
            "fundamental_score": min(score, 100.0),
            "pe_ratio": pe,
            "roe": roe
        }
      
