import os
import csv
import logging
from datetime import datetime

from config import (
    SP500_LIST_FILE,
    CONFIDENCE_THRESHOLD,
    MAX_ALERTS_PER_RUN,
    TELEGRAM_BOT_TOKEN
)
from data_fetcher import DataFetcher
from technical_analysis import TechnicalAnalyzer
from fundamental_analysis import FundamentalAnalyzer
from macro_analysis import MacroAnalyzer
from scoring import ScoringEngine
from telegram_sender import TelegramSender

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_sp500_tickers():
    tickers_list = []
    try:
        csv_path = SP500_LIST_FILE
        if not os.path.exists(csv_path):
            csv_path = "data/sp500_list.csv"

        if not os.path.exists(csv_path):
            logger.error(f"No se encontró el archivo de empresas en {csv_path}")
            return []

        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticker = row.get("ticker", "").strip()
                company_name = row.get("company_name", "").strip()
                if ticker:
                    tickers_list.append({"ticker": ticker, "company_name": company_name})
                    
        logger.info(f"Se cargaron {len(tickers_list)} empresas para análisis.")
        return tickers_list
    except Exception as e:
        logger.error(f"Error cargando lista de tickers: {str(e)}")
        return []

def main():
    logger.info("=== INICIANDO ANÁLISIS DE MERCADO S&P 500 ===")
    
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    
    fetcher = DataFetcher()
    sender = TelegramSender()
    
    tickers = load_sp500_tickers()
    if not tickers:
        logger.error("No hay tickers para analizar. Saliendo...")
        return

    opportunities = []

    for item in tickers:
        ticker = item["ticker"]
        company_name = item["company_name"]
        
        logger.info(f"Analizando {ticker} - {company_name}...")

        try:
            df_history = fetcher.get_stock_data(ticker, period="60d")
            if df_history is None or len(df_history) < 50:
                continue
            
            tech_analyzer = TechnicalAnalyzer(df_history)
            tech_result = tech_analyzer.calculate_all_indicators()
            if not tech_result:
                continue

            fund_data = fetcher.get_fundamental_data(ticker)
            analyst_ratings = fetcher.get_analyst_ratings(ticker)
            
            fund_analyzer = FundamentalAnalyzer(fund_data, analyst_ratings)
            fund_result = fund_analyzer.evaluate_fundamentals()

            news_articles = fetcher.get_recent_news(ticker, days=7)
            macro_analyzer = MacroAnalyzer(news_articles)
            macro_result = macro_analyzer.evaluate_macro_and_news()

            liquidity_score = fetcher.check_liquidity(ticker)

            scoring_engine = ScoringEngine(tech_result, fund_result, macro_result, liquidity_score)
            score_data = scoring_engine.calculate_final_score()

            logger.info(f"Resultado {ticker}: Puntaje = {score_data.get('final_score', 0)}")

            if score_data.get("included", False):
                opportunities.append({
                    "ticker": ticker,
                    "company_name": company_name,
                    "current_price": tech_result.get("current_price", 0),
                    "score_data": score_data,
                    "technical_data": tech_result
                })

        except Exception as e:
            logger.error(f"Error procesando el ticker {ticker}: {str(e)}")
            continue

    opportunities.sort(key=lambda x: x["score_data"]["final_score"], reverse=True)
    top_opportunities = opportunities[:MAX_ALERTS_PER_RUN]

    if top_opportunities and chat_id:
        for opp in top_opportunities:
            sender.send_alert_message(
                chat_id=chat_id,
                company_name=opp["company_name"],
                ticker=opp["ticker"],
                current_price=opp["current_price"],
                score_data=opp["score_data"],
                technical_data=opp["technical_data"]
            )
    else:
        logger.info("No hay suficientes oportunidades o falta configurar TELEGRAM_CHAT_ID.")

    logger.info("=== ANÁLISIS FINALIZADO ===")

if __name__ == "__main__":
    main()
          
