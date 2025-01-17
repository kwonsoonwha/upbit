import pandas as pd
import datetime
import logging
from config.config import *

class TradeHistory:
    @staticmethod
    def save_trade(trade_type, ticker, price, amount):
        """거래 기록 저장"""
        try:
            data = {
                'datetime': datetime.datetime.now(),
                'type': trade_type,
                'ticker': ticker,
                'price': price,
                'amount': amount
            }
            
            df = pd.DataFrame([data])
            df.to_csv(TRADE_HISTORY_FILE, mode='a', header=False, index=False)
            logging.info(f"거래 기록 저장: {trade_type} {ticker} {price} {amount}")
            
        except Exception as e:
            logging.error(f"거래 기록 저장 실패: {e}")

def calculate_profit(buy_price, current_price):
    """수익률 계산"""
    if buy_price is None or current_price is None:
        return 0
    
    return ((current_price - buy_price) / buy_price) * 100

def format_currency(amount):
    """금액 포맷팅"""
    return format(int(amount), ',') + '원' 