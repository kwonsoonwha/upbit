import pandas as pd
import pyupbit
import logging
from config.config import *

class TradingStrategy:
    @staticmethod
    def get_ma_crossover_signal(ticker, short_window=5, long_window=20):
        """이동평균선 크로스오버 전략"""
        try:
            df = pyupbit.get_ohlcv(ticker, interval="minute5")
            if df is None:
                return None
                
            df['short_ma'] = df['close'].rolling(window=short_window).mean()
            df['long_ma'] = df['close'].rolling(window=long_window).mean()
            
            # 골든 크로스 (단기선이 장기선을 상향 돌파)
            if df['short_ma'].iloc[-2] < df['long_ma'].iloc[-2] and \
               df['short_ma'].iloc[-1] >= df['long_ma'].iloc[-1]:
                logging.info(f"골든 크로스 발생: {ticker}")
                return "BUY"
            
            # 데드 크로스 (단기선이 장기선을 하향 돌파)
            elif df['short_ma'].iloc[-2] > df['long_ma'].iloc[-2] and \
                 df['short_ma'].iloc[-1] <= df['long_ma'].iloc[-1]:
                logging.info(f"데드 크로스 발생: {ticker}")
                return "SELL"
                
            return None
            
        except Exception as e:
            logging.error(f"전략 실행 중 오류 발생: {e}")
            return None

    @staticmethod
    def check_stop_loss(current_price, buy_price):
        """손절 가격 확인"""
        if buy_price is None:
            return False
        
        loss_ratio = (current_price - buy_price) / buy_price
        if loss_ratio <= -STOP_LOSS:
            logging.info(f"손절 조건 도달: 손실률 {loss_ratio:.2%}")
            return True
        return False 