class FundamentalAnalyzer:
    def __init__(self, fund_data: dict, analyst_ratings: dict):
        self.fund_data = fund_data or {}
        self.analyst_ratings = analyst_ratings or {}

    def evaluate_fundamentals(self):
        """
        Evalúa de forma integral métricas financieras clave:
        EPS, P/E, PEG, ROE, ROIC, Flujo de Caja Libre, Crecimiento de Ingresos, Márgenes y Deuda.
        """
        score = 50.0  # Base neutra
        details = []

        # Extraer métricas de yfinance de forma segura
        trailing_pe = self.fund_data.get("trailingPE")
        peg_ratio = self.fund_data.get("pegRatio")
        roe = self.fund_data.get("returnOnEquity")
        roic = self.fund_data.get("returnOnCapital") # O ROIC si viene expuesto
        free_cash_flow = self.fund_data.get("freeCashflow")
        revenue_growth = self.fund_data.get("revenueGrowth")
        profit_margins = self.fund_data.get("profitMargins")
        operating_margins = self.fund_data.get("operatingMargins")
        debt_to_equity = self.fund_data.get("debtToEquity")
        earnings_growth = self.fund_data.get("earningsGrowth")

        # 1. Crecimiento de Ganancias / EPS
        if earnings_growth is not None:
            if earnings_growth > 0.15:
                score += 8.0
                details.append("Crecimiento de ganancias fuerte (>15%)")
            elif earnings_growth > 0.05:
                score += 4.0
                details.append("Crecimiento de ganancias moderado")
            elif earnings_growth < 0:
                score -= 8.0
                details.append("Crecimiento de ganancias negativo")

        # 2. Valoración Relativa (P/E y PEG)
        if trailing_pe is not None:
            if 0 < trailing_pe < 22:
                score += 6.0
                details.append(f"P/E atractivo ({trailing_pe:.1f})")
            elif trailing_pe > 45:
                score -= 6.0
                details.append(f"P/E elevado/caro ({trailing_pe:.1f})")

        if peg_ratio is not None:
            if 0 < peg_ratio < 1.5:
                score += 6.0
                details.append(f"PEG favorable ({peg_ratio:.2f})")
            elif peg_ratio > 2.5:
                score -= 4.0
                details.append(f"PEG alto ({peg_ratio:.2f})")

        # 3. Rentabilidad de Calidad (ROE)
        if roe is not None:
            if roe > 0.15:  # Mayor al 15%
                score += 8.0
                details.append(f"ROE sólido ({roe*100:.1f}%)")
            elif roe < 0.05:
                score -= 5.0
                details.append(f"ROE bajo ({roe*100:.1f}%)")

        # 4. Flujo de Caja Libre (FCF)
        if free_cash_flow is not None:
            if free_cash_flow > 0:
                score += 6.0
                details.append("Flujo de caja libre positivo")
            else:
                score -= 8.0
                details.append("Flujo de caja libre negativo")

        # 5. Crecimiento de Ingresos (Revenue Growth)
        if revenue_growth is not None:
            if revenue_growth > 0.10:
                score += 6.0
                details.append(f"Crecimiento de ingresos fuerte ({revenue_growth*100:.1f}%)")
            elif revenue_growth < 0:
                score -= 6.0
                details.append("Ingresos en retroceso")

        # 6. Márgenes (Neto y Operativo)
        if profit_margins is not None:
            if profit_margins > 0.15:
                score += 6.0
                details.append(f"Margen neto excelente ({profit_margins*100:.1f}%)")
            elif profit_margins < 0.05:
                score -= 4.0
                details.append("Margen neto ajustado")

        if operating_margins is not None:
            if operating_margins > 0.20:
                score += 4.0
                details.append("Margen operativo robusto")

        # 7. Salud Financiera (Deuda / Equity)
        if debt_to_equity is not None:
            # yfinance suele dar debtToEquity en porcentaje (ej: 150.0 significa 1.5)
            d_e_normalized = debt_to_equity / 100.0 if debt_to_equity > 10 else debt_to_equity
            if d_e_normalized < 1.0:
                score += 6.0
                details.append("Salud del balance sólida (Baja deuda)")
            elif d_e_normalized > 2.5:
                score -= 8.0
                details.append(f"Alto nivel de endeudamiento (D/E: {d_e_normalized:.1f})")

        # Asegurar que el puntaje final se mantenga entre 0 y 100
        final_fundamental_score = max(0.0, min(100.0, score))

        return {
            "fundamental_score": round(final_fundamental_score, 2),
            "details": details
            }
            
