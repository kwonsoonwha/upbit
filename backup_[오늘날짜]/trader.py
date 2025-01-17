import pyupbit
import logging
from datetime import datetime

class UpbitTrader:
    def __init__(self):
        self.upbit = None
        self.running = False
        self.logger = logging.getLogger(__name__)
        self.coin = "KRW-BTC"
        self.trading_status = "대기중"
        self.last_analysis = {}
        self.last_signal = None
        self.trade_count = 0

    def set_api_keys(self, access, secret):
        """API 키 설정"""
        try:
            self.upbit = pyupbit.Upbit(access, secret)
            self.logger.info("업비트 API 연동 성공")
            return True
        except Exception as e:
            self.logger.error(f"업비트 API 연동 실패: {str(e)}")
            return False

    def get_current_price(self, coin=None):
        """현재가 조회"""
        try:
            if coin is None:
                coin = self.coin
            ticker = pyupbit.get_current_price(coin)
            
            # 현재가, 변동률, 거래량을 함께 반환
            return {
                'trade_price': ticker,
                'change_rate': self._get_change_rate(coin),
                'acc_trade_volume_24h': self._get_24h_volume(coin)
            }
        except Exception as e:
            self.logger.error(f"현재가 조회 실패: {str(e)}")
            return None

    def _get_change_rate(self, coin):
        """24시간 변동률 조회"""
        try:
            # get_ticker 대신 get_ohlcv 사용
            df = pyupbit.get_ohlcv(coin, interval="day", count=1)
            if df is not None and not df.empty:
                open_price = df.iloc[0]['open']
                close_price = df.iloc[0]['close']
                return (close_price - open_price) / open_price
            return 0.0
        except Exception as e:
            self.logger.error(f"변동률 조회 실패: {str(e)}")
            return 0.0

    def _get_24h_volume(self, coin):
        """24시간 거래량 조회"""
        try:
            # get_ticker 대신 get_ohlcv 사용
            df = pyupbit.get_ohlcv(coin, interval="day", count=1)
            if df is not None and not df.empty:
                return df.iloc[0]['volume']
            return 0.0
        except Exception as e:
            self.logger.error(f"거래량 조회 실패: {str(e)}")
            return 0.0

    def get_balance(self, coin=None):
        """잔고 조회"""
        try:
            if self.upbit is None:
                return None
                
            if coin is None:
                coin = self.coin
                
            coin_symbol = coin.split('-')[1]  # KRW-BTC -> BTC
            
            # KRW 잔고
            krw_balance = self.upbit.get_balance("KRW")
            # 코인 잔고
            coin_balance = self.upbit.get_balance(coin)
            # 코인 평가금액
            coin_value = coin_balance * self.get_current_price(coin)['trade_price'] if coin_balance else 0
            
            # 총 평가금액
            total_value = krw_balance + coin_value
            
            # 초기 투자금액 (또는 매수 평균가) - 실제 구현 필요
            initial_investment = total_value  # 임시로 동일하게 설정
            
            return {
                'krw': krw_balance,
                'coin_amount': coin_balance,
                'coin_value': coin_value,
                'total_value': total_value,
                'profit_rate': ((total_value - initial_investment) / initial_investment * 100) 
                              if initial_investment > 0 else 0.0
            }
        except Exception as e:
            self.logger.error(f"잔고 조회 실패: {str(e)}")
            return None

    def start_auto_trading(self, strategy_key, settings):
        try:
            self.coin = settings['coin']
            self.amount = settings['amount']
            self.strategy_key = strategy_key
            self.running = True
            self.trading_status = "시작됨"
            self.last_analysis = {}
            self.last_signal = None
            self.trade_count = 0
            
            # 시작 로그
            self.logger.info(f"자동매매 시작 - 코인: {self.coin}, 금액: {self.amount:,}원, 전략: {strategy_key}")
            return True
            
        except Exception as e:
            self.logger.error(f"자동매매 시작 실패: {str(e)}")
            return False

    def analyze_market(self):
        """시장 분석"""
        try:
            self.trading_status = "차트 분석중..."
            current_price = self.get_current_price(self.coin)
            
            # 전략별 매수/매도 가격 계산
            if self.strategy_key == 'RSI':
                target_buy = current_price['trade_price'] * 0.98  # 예: 현재가 대비 2% 하락 시 매수
                target_sell = current_price['trade_price'] * 1.02  # 예: 현재가 대비 2% 상승 시 매도
            else:
                # 다른 전략들에 대한 매수/매도 가격 계산 로직
                target_buy = current_price['trade_price'] * 0.99
                target_sell = current_price['trade_price'] * 1.01
                
            self.last_analysis = {
                'current_price': current_price['trade_price'],
                'target_buy': target_buy,
                'target_sell': target_sell,
                'rsi': 65.5,  # 예시 값
                'macd': 'POSITIVE',
                'volume': '증가중',
                'trend': '상승추세'
            }
            self.trading_status = "매매 신호 대기중..."
            return True
            
        except Exception as e:
            self.trading_status = f"분석 실패: {str(e)}"
            return False

    def check_trading_signal(self):
        """매매 신호 확인"""
        try:
            current_price = self.get_current_price(self.coin)
            if current_price:
                # 여기에 실제 신호 확인 로직 추가
                self.last_signal = {
                    'type': 'BUY',  # 또는 'SELL'
                    'price': current_price['trade_price'],
                    'reason': 'RSI 과매도 구간'
                }
            return True
        except Exception as e:
            self.trading_status = f"신호 확인 실패: {str(e)}"
            return False

    def get_current_status(self):
        """현재 상태 조회"""
        try:
            if not self.running:
                return {
                    'main_status': '대기중',
                    'details': '자동매매가 시작되지 않았습니다.'
                }
            
            details = []
            details.append(f"상태: {self.trading_status}")
            details.append(f"코인: {self.coin}")
            
            if self.last_analysis:
                details.append(f"\n매매 계획:")
                details.append(f"현재가: {self.last_analysis['current_price']:,}원")
                details.append(f"매수 목표가: {self.last_analysis['target_buy']:,.0f}원")
                details.append(f"매도 목표가: {self.last_analysis['target_sell']:,.0f}원")
                
                details.append(f"\n시장 분석:")
                details.append(f"RSI: {self.last_analysis['rsi']}")
                details.append(f"MACD: {self.last_analysis['macd']}")
                details.append(f"거래량 추세: {self.last_analysis['volume']}")
                details.append(f"가격 추세: {self.last_analysis['trend']}")
            
            if self.last_signal:
                details.append(f"\n매매 신호:")
                details.append(f"유형: {self.last_signal['type']}")
                details.append(f"가격: {self.last_signal['price']:,}원")
                details.append(f"사유: {self.last_signal['reason']}")
            
            # 계좌 정보 조회
            balance_info = self.get_balance()
            if balance_info:
                details.append(f"\n계좌 정보:")
                details.append(f"보유 KRW: {balance_info['krw']:,}원")
                details.append(f"보유 코인: {balance_info['coin_amount']} {self.coin}")
                details.append(f"총 평가액: {balance_info['total_value']:,}원")
                details.append(f"수익률: {balance_info['profit_rate']:+.2f}%")
            
            details.append(f"\n매매 설정:")
            details.append(f"전략: {self.strategy_key}")
            details.append(f"매매금액: {self.amount:,}원")
            details.append(f"총 거래 횟수: {self.trade_count}회")
            
            return {
                'main_status': self.trading_status,
                'details': '\n'.join(details)
            }
                
        except Exception as e:
            self.logger.error(f"상태 조회 실패: {str(e)}")
            return {
                'main_status': '오류 발생',
                'details': f'상태 조회 실패: {str(e)}'
            }

    def stop_auto_trading(self):
        """자동매매 중지"""
        try:
            self.running = False
            self.trading_status = "중지됨"
            self.logger.info("자동매매 중지")
            return True
            
        except Exception as e:
            self.logger.error(f"자동매매 중지 실패: {str(e)}")
            return False