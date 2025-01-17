import os
import json
import logging
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QTextEdit,
                           QGroupBox, QRadioButton, QScrollArea, QMessageBox,
                           QGridLayout, QDialog, QComboBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from .config import STRATEGIES

class StrategyInfoDialog(QDialog):
    def __init__(self, strategy_key, parent=None):
        super().__init__(parent)
        self.strategy_key = strategy_key
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(f'전략 상세 정보 - {STRATEGIES[self.strategy_key]["name"]}')
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # 스크롤 영역 생성
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout()
        
        # 전략 설명 추가
        title = QLabel(STRATEGIES[self.strategy_key]["name"])
        title.setFont(QFont('Arial', 14, QFont.Bold))
        content_layout.addWidget(title)
        
        desc = QLabel(STRATEGIES[self.strategy_key]["desc"])
        desc.setWordWrap(True)
        content_layout.addWidget(desc)
        
        # 상세 설명
        details = QLabel(self.get_strategy_details())
        details.setWordWrap(True)
        content_layout.addWidget(details)
        
        # 예시 이미지나 차트 추가 가능
        
        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # 닫기 버튼
        close_btn = QPushButton('닫기')
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        
    def get_strategy_details(self):
        details = {
            'RSI': """
            RSI(상대강도지수) 전략
            
            1. 개요
            - RSI는 가격의 상승압력과 하락압력을 비교하여 과매수/과매도 구간을 판단
            - 0부터 100까지의 범위를 가지며, 일반적으로 30/70을 기준으로 함
            
            2. 매매 신호
            - 매수 신호: RSI가 30 이하로 진입할 때
            - 매도 신호: RSI가 70 이상으로 진입할 때
            
            3. 장점
            - 과매수/과매도 구간을 명확하게 파악 가능
            - 모멘텀 반전 시점 포착에 유용
            
            4. 단점
            - 강한 추세장에서는 빈번한 허위 신호 발생 가능
            - 지표 후행성으로 인한 진입/청산 시점 지연
            
            5. 파라미터
            - 기간: 14일 (기본값)
            - 과매도 기준: 30
            - 과매수 기준: 70
            """,
            
            'MACD': """
            MACD(이동평균수렴확산) 전략
            
            1. 개요
            - 단기와 장기 이동평균의 차이를 이용한 추세 추종 지표
            - MACD선과 신호선의 교차를 통해 매매 시점 포착
            
            2. 매매 신호
            - 매수 신호: MACD선이 신호선을 상향돌파할 때
            - 매도 신호: MACD선이 신호선을 하향돌파할 때
            
            3. 장점
            - 추세의 방향과 강도를 동시에 파악 가능
            - 중장기 추세 추종에 적합
            
            4. 단점
            - 횡보장에서는 효과가 떨어짐
            - 지표의 후행성이 있음
            
            5. 파라미터
            - 단기 EMA: 12일
            - 장기 EMA: 26일
            - 신호선: 9일
            """,
            
            'BB': """
            볼린저 밴드(Bollinger Bands) 전략
            
            1. 개요
            - 이동평균선을 중심으로 표준편차를 이용해 상하한 밴드를 설정
            - 가격 변동성과 추세를 동시에 파악 가능
            
            2. 매매 신호
            - 매수 신호: 가격이 하단 밴드 하향 돌파 후 반등
            - 매도 신호: 가격이 상단 밴드 상향 돌파 후 반락
            
            3. 장점
            - 변동성에 따른 동적 지지/저항 레벨 제공
            - 과매수/과매도 구간 식별 용이
            
            4. 단점
            - 강한 추세장에서는 잦은 신호 발생
            - 변동성 급변 시 대응 지연
            
            5. 파라미터
            - 이동평균 기간: 20일
            - 표준편차 승수: 2
            """,
            
            'SMA': """
            단순이동평균(Simple Moving Average) 전략
            
            1. 개요
            - 여러 기간의 이동평균선을 이용한 추세 추종
            - 골든크로스/데드크로스 활용
            
            2. 매매 신호
            - 매수 신호: 단기선이 장기선을 상향돌파(골든크로스)
            - 매도 신호: 단기선이 장기선을 하향돌파(데드크로스)
            
            3. 장점
            - 이해하기 쉽고 명확한 신호
            - 중장기 추세 파악에 유용
            
            4. 단점
            - 시차가 존재하여 진입/청산 시점 지연
            - 횡보장에서 잦은 허위 신호
            
            5. 파라미터
            - 단기 이동평균: 5일
            - 중기 이동평균: 20일
            - 장기 이동평균: 60일
            """,
            
            'VWAP': """
            거래량가중평균가격(VWAP) 전략
            
            1. 개요
            - 거래량을 고려한 평균 가격을 산출
            - 기관투자자들의 매매 기준선으로 활용
            
            2. 매매 신호
            - 매수 신호: 가격이 VWAP 상향돌파
            - 매도 신호: 가격이 VWAP 하향돌파
            
            3. 장점
            - 거래량 반영으로 더 신뢰성 있는 지표
            - 기관의 매매 동향 파악 가능
            
            4. 단점
            - 일중거래에 더 적합
            - 거래량이 적은 종목에서는 신뢰성 하락
            
            5. 파라미터
            - 계산 기간: 일반적으로 1일
            - 거래량 가중치 설정
            """,
            
            'Stochastic': """
            스토캐스틱(Stochastic) 전략
            
            1. 개요
            - 현재가가 일정 기간의 가격 범위 중 어디에 위치하는지 판단
            - %K와 %D 두 개의 선을 이용
            
            2. 매매 신호
            - 매수 신호: %K가 %D를 상향돌파하며 과매도 구간 이탈
            - 매도 신호: %K가 %D를 하향돌파하며 과매수 구간 이탈
            
            3. 장점
            - 가격 모멘텀과 반전 시점 포착에 유용
            - RSI와 함께 사용 시 시너지 효과
            
            4. 단점
            - 빈번한 신호 발생
            - 강한 추세장에서는 부적합
            
            5. 파라미터
            - %K 기간: 14일
            - %D 기간: 3일
            - 과매수/과매도 기준: 80/20
            """,
            
            'Ichimoku': """
            일목균형표(Ichimoku) 전략
            
            1. 개요
            - 일본에서 개발된 종합적인 기술적 분석 도구
            - 여러 지표를 동시에 표시하여 추세와 지지/저항 분석
            
            2. 매매 신호
            - 매수 신호: 전환선이 기준선을 상향돌파, 구름대 상향돌파
            - 매도 신호: 전환선이 기준선을 하향돌파, 구름대 하향돌파
            
            3. 장점
            - 다양한 시간대의 추세를 한번에 파악
            - 미래의 지지/저항 레벨 예측 가능
            
            4. 단점
            - 다소 복잡한 지표 구성
            - 초보자가 이해하기 어려움
            
            5. 파라미터
            - 전환선: 9일
            - 기준선: 26일
            - 선행스팬: 26일
            - 후행스팬: 26일
            """,
            
            'SuperTrend': """
            수퍼트렌드(SuperTrend) 전략
            
            1. 개요
            - ATR을 기반으로 한 추세 추종 지표
            - 명확한 매매 신호 제공
            
            2. 매매 신호
            - 매수 신호: 가격이 수퍼트렌드 선을 상향돌파
            - 매도 신호: 가격이 수퍼트렌드 선을 하향돌파
            
            3. 장점
            - 추세 방향 명확히 제시
            - 손절 라인으로도 활용 가능
            
            4. 단점
            - 횡보장에서 잦은 신호 발생
            - ATR 변동성에 따른 민감도 차이
            
            5. 파라미터
            - ATR 기간: 10일
            - ATR 승수: 3
            """,
            
            'DMI': """
            DMI/ADX(방향성 지수) 전략
            
            1. 개요
            - 추세의 방향과 강도를 동시에 측정
            - +DI, -DI, ADX 세 개의 지표 활용
            
            2. 매매 신호
            - 매수 신호: +DI가 -DI를 상향돌파하고 ADX가 상승
            - 매도 신호: -DI가 +DI를 상향돌파하고 ADX가 상승
            
            3. 장점
            - 추세의 강도까지 고려한 매매
            - 허위 신호 감소
            
            4. 단점
            - 계산이 다소 복잡
            - 신호 발생이 다소 늦을 수 있음
            
            5. 파라미터
            - DI 기간: 14일
            - ADX 기간: 14일
            """,
            
            'Williams': """
            윌리엄스 %R 전략
            
            1. 개요
            - 일정 기간의 고가/저가 대비 현재가 위치 측정
            - 스토캐스틱과 유사하나 계산 방식 차이
            
            2. 매매 신호
            - 매수 신호: %R이 -80 이하에서 상승 반전
            - 매도 신호: %R이 -20 이상에서 하락 반전
            
            3. 장점
            - 과매수/과매도 구간 명확
            - 가격 반전 시점 포착에 유용
            
            4. 단점
            - 단독 사용 시 허위 신호 가능성
            - 강한 추세장에서는 부적합
            
            5. 파라미터
            - 기간: 14일
            - 과매수/과매도: -20/-80
            """,
            
            'TrendFollow': """
            추세추종(Trend Following) 전략
            
            1. 개요
            - MACD와 RSI를 결합한 복합 전략
            - 추세 확인 후 진입 시점 결정
            
            2. 매매 신호
            - 매수 신호: MACD 상향돌파 + RSI 상승 반전
            - 매도 신호: MACD 하향돌파 + RSI 하락 반전
            
            3. 장점
            - 두 지표의 시너지 효과
            - 허위 신호 감소
            
            4. 단점
            - 신호 발생 빈도 감소
            - 진입 시점 다소 지연
            
            5. 파라미터
            - MACD 설정값 활용
            - RSI 설정값 활용
            """,
            
            'VolBreakout': """
            변동성 돌파(Volatility Breakout) 전략
            
            1. 개요
            - 전일 변동성을 기준으로 매수/매도 포인트 설정
            - 변동성 증가 구간을 활용
            
            2. 매매 신호
            - 매수 신호: 당일 고가가 기준가격 상향돌파
            - 매도 신호: 당일 저가가 기준가격 하향돌파
            
            3. 장점
            - 변동성에 따른 탄력적 대응
            - 추세 초기 진입 가능
            
            4. 단점
            - 변동성 급변 시 리스크 증가
            - 거래 비용 증가 가능
            
            5. 파라미터
            - 변동성 계수: 0.5
            - ATR 기간: 14일
            """,
            
            'MultiMA': """
            복합이동평균(Multiple Moving Average) 전략
            
            1. 개요
            - 3개 이상의 이동평균선을 활용
            - 단기/중기/장기 추세 동시 분석
            
            2. 매매 신호
            - 매수 신호: 단기선이 중장기선 모두 상향돌파
            - 매도 신호: 단기선이 중장기선 모두 하향돌파
            
            3. 장점
            - 다중 확인으로 신뢰도 향상
            - 추세 강도 파악 용이
            
            4. 단점
            - 신호 발생 지연
            - 약세장/횡보장에서 부적합
            
            5. 파라미터
            - 단기선: 5일
            - 중기선: 20일
            - 장기선: 60일
            """,
            
            'MomentumRev': """
            모멘텀 반전(Momentum Reversal) 전략
            
            1. 개요
            - RSI와 스토캐스틱을 결합한 반전 포착
            - 과매수/과매도 구간에서의 반전 노림
            
            2. 매매 신호
            - 매수 신호: RSI와 스토캐스틱 모두 과매도에서 반등
            - 매도 신호: RSI와 스토캐스틱 모두 과매수에서 반락
            
            3. 장점
            - 정확한 반전 시점 포착
            - 두 지표의 교차 검증
            
            4. 단점
            - 신호 발생 빈도 낮음
            - 강한 추세장에서 불리
            
            5. 파라미터
            - RSI 설정값
            - 스토캐스틱 설정값
            """,
            
            'VolumeBreak': """
            거래량 돌파(Volume Breakout) 전략
            
            1. 개요
            - 거래량과 가격 변동의 상관관계 활용
            - 거래량 급증 구간에서의 매매 시도
            
            2. 매매 신호
            - 매수 신호: 거래량 급증 + 양봉 발생
            - 매도 신호: 거래량 급증 + 음봉 발생
            
            3. 장점
            - 시장 참여자 증가 구간 포착
            - 추세 전환 조기 발견
            
            4. 단점
            - 허위 신호 발생 가능
            - 거래량 조작에 취약
            
            5. 파라미터
            - 거래량 증가율: 200%
            - 이동평균 기간: 20일
            """,
            
            'AI_Basic': """
            AI 기본 전략
            
            1. 개요
            - 기본적인 기술적 지표들의 AI 기반 분석
            - 단순한 규칙 기반의 학습 모델 적용
            
            2. 분석 요소
            - RSI, MACD, 볼린저밴드 기본 지표
            - 거래량 데이터
            - 가격 변동성
            
            3. 매매 결정
            - 지표들의 가중 평균으로 신호 생성
            - 기본적인 머신러닝 모델 적용
            
            4. 장점
            - 기본적인 패턴 학습
            - 단순하고 안정적인 운영
            
            5. 단점
            - 복잡한 시장 상황 대응 한계
            - 제한적인 학습 능력
            """,
            
            'AI_Advanced': """
            AI 고급 전략
            
            1. 개요
            - 다양한 지표와 패턴의 복합 분석
            - 심층 학습 모델 적용
            
            2. 분석 요소
            - 기본 지표 + VWAP, ATR 등 고급 지표
            - 시장 심리 지표
            - 추세 강도 분석
            
            3. 매매 결정
            - 다층 신경망 기반 의사결정
            - 리스크 관리 로직 포함
            
            4. 장점
            - 복잡한 패턴 인식 가능
            - 시장 상황별 대응 능력
            
            5. 단점
            - 과적합 위험
            - 많은 학습 데이터 필요
            """,
            
            'AI_Full': """
            AI 풀 전략
            
            1. 개요
            - 종합적인 시장 분석과 AI 의사결정
            - 딥러닝과 강화학습 결합
            
            2. 분석 요소
            기본 지표:
            - RSI, MACD, 볼린저밴드
            
            고급 지표:
            - VWAP, ATR, 추세 강도
            
            시장 분석:
            - 변동성 분석
            - 모멘텀 분석
            - 시장 국면 분석
            
            3. 매매 결정 프로세스
            - 각 지표별 신호 수집
            - 딥러닝 기반 패턴 인식
            - 강화학습 기반 매매 결정
            - 신뢰도 70% 이상 시 매매
            
            4. 학습 시스템
            - 실시간 데이터 학습
            - 성공/실패 피드백
            - 동적 가중치 조정
            - 최대 1000개 데이터 저장
            
            5. 장점
            - 종합적 시장 분석
            - 자가 학습 및 개선
            - 리스크 관리 강화
            
            6. 단점
            - 초기 학습에 시간 소요
            - 높은 컴퓨팅 파워 필요
            - 블랙박스 의사결정
            
            7. 특수 기능
            - 이상치 감지
            - 시장 스트레스 테스트
            - 포트폴리오 최적화
            """
        }
        return details.get(self.strategy_key, "상세 설명이 준비되지 않았습니다.")

class UpbitTradingUI(QMainWindow):
    def __init__(self, trader):
        super().__init__()
        self.trader = trader
        self.logger = logging.getLogger(__name__)
        self.coin = 'KRW-BTC'  # 기본 코인 설정
        self.config_file = 'config/api_keys.json'
        self.init_ui()
        self.load_api_keys()

    def init_ui(self):
        self.setWindowTitle('Upbit Trading Bot - Developer Mode')
        self.setGeometry(100, 100, 1200, 800)

        # 메인 위젯과 레이아웃
        main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

        # API 키 입력 그룹
        api_group = QGroupBox('API 설정')
        api_layout = QGridLayout()
        
        self.access_key = QLineEdit()
        self.secret_key = QLineEdit()
        self.secret_key.setEchoMode(QLineEdit.Password)
        
        api_layout.addWidget(QLabel('Access Key:'), 0, 0)
        api_layout.addWidget(self.access_key, 0, 1)
        api_layout.addWidget(QLabel('Secret Key:'), 1, 0)
        api_layout.addWidget(self.secret_key, 1, 1)
        
        # API 키 저장 버튼 추가
        api_save_btn = QPushButton('API 키 저장')
        api_save_btn.clicked.connect(self.save_api_keys)
        api_layout.addWidget(api_save_btn, 2, 1)

        # API 키 연동 버튼 추가
        api_connect_btn = QPushButton('업비트 연동')
        api_connect_btn.clicked.connect(self.connect_upbit)
        api_layout.addWidget(api_connect_btn, 2, 0)
        
        api_group.setLayout(api_layout)
        self.main_layout.addWidget(api_group)

        # 거래 설정 그룹 (새로 추가)
        trade_config_group = QGroupBox('거래 설정')
        trade_layout = QGridLayout()
        
        # 코인 선택 콤보박스
        self.coin_combo = QComboBox()
        self.coin_combo.addItems([
            'KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-DOGE', 'KRW-ADA',
            'KRW-MATIC', 'KRW-SOL', 'KRW-DOT', 'KRW-AVAX'
        ])
        self.coin_combo.currentTextChanged.connect(self.on_coin_changed)
        trade_layout.addWidget(QLabel('거래 코인:'), 0, 0)
        trade_layout.addWidget(self.coin_combo, 0, 1)
        
        # 매매 금액 설정
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('거래금액 입력 (KRW)')
        trade_layout.addWidget(QLabel('매매 금액:'), 1, 0)
        trade_layout.addWidget(self.amount_input, 1, 1)
        
        trade_config_group.setLayout(trade_layout)
        self.main_layout.addWidget(trade_config_group)

        # 기존 시장 정보 그룹
        market_group = QGroupBox('시장 정보')
        market_layout = QGridLayout()
        
        self.current_price_label = QLabel('현재가: --')
        self.current_price_label.setStyleSheet('font-size: 14pt; font-weight: bold;')
        self.change_label = QLabel('24시간 변동: --')
        self.volume_label = QLabel('거래량: --')
        
        market_layout.addWidget(self.current_price_label, 0, 0)
        market_layout.addWidget(self.change_label, 0, 1)
        market_layout.addWidget(self.volume_label, 1, 0)
        
        market_group.setLayout(market_layout)
        self.main_layout.addWidget(market_group)

        # 기존 계좌 정보 그룹
        account_group = QGroupBox('계좌 정보')
        account_layout = QGridLayout()
        
        self.krw_label = QLabel('보유 KRW: --')
        self.coin_amount_label = QLabel('보유 코인: --')
        self.total_value_label = QLabel('총 평가액: --')
        self.profit_label = QLabel('수익률: --')
        
        account_layout.addWidget(self.krw_label, 0, 0)
        account_layout.addWidget(self.coin_amount_label, 0, 1)
        account_layout.addWidget(self.total_value_label, 1, 0)
        account_layout.addWidget(self.profit_label, 1, 1)
        
        account_group.setLayout(account_layout)
        self.main_layout.addWidget(account_group)

        # 기존 전략 선택 그룹 (스크롤 영역 포함)
        strategy_group = QGroupBox('투자 전략 선택')
        strategy_layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.strategy_layout = QVBoxLayout()
        
        # 기존 전략 라디오 버튼들
        for key, value in STRATEGIES.items():
            row_layout = QHBoxLayout()
            
            rb = QRadioButton(value['name'])
            rb.setStyleSheet('font-size: 11pt;')
            rb.setProperty('strategy_key', key)
            row_layout.addWidget(rb)
            
            info_btn = QPushButton('ℹ️ 상세정보')
            info_btn.setStyleSheet('''
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    max-width: 80px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            ''')
            info_btn.setProperty('strategy_key', key)
            info_btn.clicked.connect(self.show_strategy_info)
            row_layout.addWidget(info_btn)
            
            desc_label = QLabel(value['desc'])
            desc_label.setStyleSheet('color: #666666; font-size: 10pt;')
            row_layout.addWidget(desc_label)
            
            row_layout.addStretch()
            self.strategy_layout.addLayout(row_layout)
        
        scroll_content.setLayout(self.strategy_layout)
        scroll.setWidget(scroll_content)
        strategy_layout.addWidget(scroll)
        strategy_group.setLayout(strategy_layout)
        self.main_layout.addWidget(strategy_group)

        # 기존 상태 표시 영역
        status_group = QGroupBox('현재 상태')
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel('대기중...')
        self.status_label.setStyleSheet('''
            QLabel {
                font-size: 12pt;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
        ''')
        status_layout.addWidget(self.status_label)
        
        self.detail_status = QTextEdit()
        self.detail_status.setReadOnly(True)
        self.detail_status.setMinimumHeight(150)
        status_layout.addWidget(self.detail_status)
        
        status_group.setLayout(status_layout)
        self.main_layout.addWidget(status_group)

        # 기존 시작/중지 버튼
        button_layout = QHBoxLayout()
        self.start_button = QPushButton('자동매매 시작')
        self.stop_button = QPushButton('자동매매 중지')
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        self.main_layout.addLayout(button_layout)

        # 상태 업데이트 타이머 설정
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_trading_status)
        self.status_timer.setInterval(1000)  # 1초마다 업데이트

        # 버튼 이벤트 연결 추가
        self.start_button.clicked.connect(self.start_trading)
        self.stop_button.clicked.connect(self.stop_trading)

    def show_strategy_info(self):
        sender = self.sender()
        strategy_key = sender.property('strategy_key')
        dialog = StrategyInfoDialog(strategy_key, self)
        dialog.exec_()

    def update_trading_status(self):
        """거래 상태 업데이트"""
        try:
            # 기본 상태 업데이트
            self.update_status()
            
            # 자동매매 중일 때만 추가 업데이트
            if self.trader.running:
                # 시장 분석 실행
                self.trader.analyze_market()
                # 매매 신호 확인
                self.trader.check_trading_signal()
                
        except Exception as e:
            self.logger.error(f"상태 업데이트 실패: {str(e)}")

    def update_status(self):
        """상태 업데이트"""
        if not self.trader:
            return
            
        try:
            # 현재가 정보 업데이트
            market_info = self.trader.get_current_price(self.coin)
            if market_info:
                self.current_price_label.setText(f"현재가: {market_info['trade_price']:,}원")
                self.change_label.setText(f"24시간 변동: {market_info['change_rate']*100:.2f}%")
                self.volume_label.setText(f"거래량: {market_info['acc_trade_volume_24h']:,.0f}")
                
                # 가격 변동에 따른 색상 변경
                if market_info['change_rate'] > 0:
                    self.current_price_label.setStyleSheet('font-size: 14pt; font-weight: bold; color: #d60000;')
                elif market_info['change_rate'] < 0:
                    self.current_price_label.setStyleSheet('font-size: 14pt; font-weight: bold; color: #0051c7;')
            
            # 계좌 정보 업데이트
            balance = self.trader.get_balance(self.coin)
            if balance:
                self.krw_label.setText(f"보유 KRW: {balance['krw']:,}원")
                self.coin_amount_label.setText(f"보유 코인: {balance['coin_amount']} {self.coin}")
                self.total_value_label.setText(f"총 평가액: {balance['total_value']:,}원")
                
                # 수익률 계산 및 표시
                if 'profit_rate' in balance:
                    profit_rate = balance['profit_rate']
                    color = '#d60000' if profit_rate > 0 else '#0051c7'
                    self.profit_label.setStyleSheet(f'font-weight: bold; color: {color};')
                    self.profit_label.setText(f"수익률: {profit_rate:+.2f}%")
            
            # 트레이딩 상태 업데이트
            if hasattr(self.trader, 'get_current_status'):
                current_status = self.trader.get_current_status()
                self.status_label.setText(current_status['main_status'])
                self.detail_status.setText(current_status['details'])
                
        except Exception as e:
            self.logger.error(f"상태 업데이트 실패: {str(e)}")

    def load_api_keys(self):
        """저장된 API 키 불러오기"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    keys = json.load(f)
                    self.access_key.setText(keys.get('access_key', ''))
                    self.secret_key.setText(keys.get('secret_key', ''))
                    self.logger.info("API 키 로드 성공")
        except Exception as e:
            self.logger.error(f"API 키 로드 실패: {str(e)}")
            QMessageBox.warning(self, '경고', 'API 키 로드에 실패했습니다.')

    def save_api_keys(self):
        """API 키 저장"""
        try:
            # config 디렉토리가 없으면 생성
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            keys = {
                'access_key': self.access_key.text().strip(),
                'secret_key': self.secret_key.text().strip()
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(keys, f)
            
            QMessageBox.information(self, '성공', 'API 키가 저장되었습니다.')
            self.logger.info("API 키 저장 성공")
            
        except Exception as e:
            self.logger.error(f"API 키 저장 실패: {str(e)}")
            QMessageBox.warning(self, '경고', 'API 키 저장에 실패했습니다.')

    def connect_upbit(self):
        """업비트 연동"""
        try:
            access = self.access_key.text().strip()
            secret = self.secret_key.text().strip()
            
            if not access or not secret:
                QMessageBox.warning(self, '경고', 'API 키를 입력해주세요.')
                return
            
            # 업비트 연동 시도
            self.trader.set_api_keys(access, secret)
            balance = self.trader.get_balance(self.coin)
            
            if balance:
                QMessageBox.information(self, '성공', '업비트 연동에 성공했습니다.')
                self.save_api_keys()  # 성공 시 키 저장
                self.update_status()  # 상태 업데이트
            else:
                QMessageBox.warning(self, '경고', '잔고 조회에 실패했습니다.')
                
        except Exception as e:
            self.logger.error(f"업비트 연동 실패: {str(e)}")
            QMessageBox.critical(self, '오류', f'업비트 연동 실패: {str(e)}')

    def on_coin_changed(self, new_coin):
        """코인 변경 시 호출되는 메서드"""
        self.coin = new_coin
        self.trader.coin = new_coin
        self.update_status()  # 새로운 코인 정보로 상태 업데이트

    def start_trading(self):
        """자동매매 시작"""
        try:
            # 입력값 검증
            if not self.amount_input.text().strip():
                QMessageBox.warning(self, '경고', '매매 금액을 입력해주세요.')
                return
            
            # 선택된 전략 확인
            strategy_key = None
            for i in range(self.strategy_layout.count()):
                item = self.strategy_layout.itemAt(i)
                if isinstance(item, QHBoxLayout):
                    rb = item.itemAt(0).widget()
                    if rb.isChecked():
                        strategy_key = rb.property('strategy_key')
                        break
                    
            if not strategy_key:
                QMessageBox.warning(self, '경고', '투자 전략을 선택해주세요.')
                return
            
            # 거래 설정
            settings = {
                'coin': self.coin_combo.currentText(),
                'amount': float(self.amount_input.text().strip())
            }
            
            # 자동매매 시작
            if self.trader.start_auto_trading(strategy_key, settings):
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                
                # 상태 업데이트 타이머 시작
                self.status_timer.start()
                
                # 최초 분석 시작
                self.trader.analyze_market()
                self.update_trading_status()
                
                QMessageBox.information(self, '알림', '자동매매가 시작되었습니다.')
            else:
                QMessageBox.warning(self, '경고', '자동매매 시작에 실패했습니다.')
            
        except Exception as e:
            QMessageBox.critical(self, '오류', f'자동매매 시작 실패: {str(e)}')

    def stop_trading(self):
        """자동매매 중지"""
        try:
            if self.trader.stop_auto_trading():
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                self.status_timer.stop()  # 상태 업데이트 타이머 중지
                
                # 상태창 즉시 업데이트
                self.status_label.setText('대기중')
                self.detail_status.setText('자동매매가 중지되었습니다.\n\n'
                                         f'마지막 거래 코인: {self.trader.coin}\n'
                                         f'매매 금액: {self.trader.amount:,}원')
                
                QMessageBox.information(self, '알림', '자동매매가 중지되었습니다.')
            else:
                QMessageBox.warning(self, '경고', '자동매매 중지에 실패했습니다.')
            
        except Exception as e:
            QMessageBox.critical(self, '오류', f'자동매매 중지 실패: {str(e)}')