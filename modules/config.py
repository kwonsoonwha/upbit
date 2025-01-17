# 업비트 API 키 설정
UPBIT_ACCESS_KEY = "2LE0OHp2EjCrvWW1cl2EasJTB80W3OPgOzojGtnI"
UPBIT_SECRET_KEY = "lP4i9mvw8EsyQ6lL1Nu91Cix63xIZ2xh9xqWCymg"

# 코인 그룹 설정
COIN_GROUPS = {
    '메이저 코인': ['KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-SOL', 'KRW-ADA'],
    'DeFi 코인': ['KRW-AAVE', 'KRW-UNI', 'KRW-SUSHI', 'KRW-COMP', 'KRW-MKR'],
    '게임/메타버스': ['KRW-SAND', 'KRW-MANA', 'KRW-AXS', 'KRW-ENJ', 'KRW-WEMIX'],
    'Layer 2/인프라': ['KRW-MATIC', 'KRW-DOT', 'KRW-ATOM', 'KRW-AVAX', 'KRW-NEAR'],
    '신규 성장주': ['KRW-APT', 'KRW-SUI', 'KRW-INJ', 'KRW-SEI', 'KRW-BLUR'],
    '기타 알트코인': ['KRW-DOGE', 'KRW-SHIB', 'KRW-VET', 'KRW-CHZ', 'KRW-LINK']
}

# 투자 전략 설정
STRATEGIES = {
    'RSI': {'name': 'RSI 전략', 'desc': '과매수/과매도 구간 활용'},
    'MACD': {'name': 'MACD 전략', 'desc': '추세 추종'},
    'BB': {'name': '볼린저밴드', 'desc': '변동성 돌파'},
    'SMA': {'name': '이동평균선', 'desc': '골든/데드크로스'},
    'VWAP': {'name': 'VWAP', 'desc': '거래량 가중 평균가격'},
    'Stochastic': {'name': '스토캐스틱', 'desc': '모멘텀 지표'},
    'Ichimoku': {'name': '일목균형표', 'desc': '일본식 기술적 분석'},
    'SuperTrend': {'name': '수퍼트렌드', 'desc': '추세 추종'},
    'DMI': {'name': 'DMI/ADX', 'desc': '추세 강도'},
    'Williams': {'name': '윌리엄스 %R', 'desc': '모멘텀 지표'},
    'TrendFollow': {'name': '추세추종', 'desc': 'MACD + RSI'},
    'VolBreakout': {'name': '변동성돌파', 'desc': 'BB + Volume'},
    'MultiMA': {'name': '복합이평선', 'desc': '3중 이동평균'},
    'MomentumRev': {'name': '모멘텀반전', 'desc': 'RSI + Stochastic'},
    'VolumeBreak': {'name': '거래량돌파', 'desc': 'Volume + Price'},
    'AI_Basic': {'name': 'AI 기본전략', 'desc': '기본 지표 조합 AI'},
    'AI_Advanced': {'name': 'AI 고급전략', 'desc': '고급 지표 분석 AI'},
    'AI_Full': {'name': 'AI 풀전략', 'desc': '종합 시장 분석 AI'}
}

# 거래 설정
TRADE_SETTINGS = {
    'DEFAULT_AMOUNT': 100000,  # 기본 거래금액 (10만원)
    'MAX_AMOUNT': 1000000,    # 최대 거래금액 (100만원)
    'MIN_AMOUNT': 5000,       # 최소 거래금액 (5천원)
    'STOP_LOSS': 3.0,         # 손절 비율 (3%)
    'TAKE_PROFIT': 5.0,       # 익절 비율 (5%)
    'USE_STOP_LOSS': True,    # 손절 사용 여부
    'USE_TAKE_PROFIT': True,  # 익절 사용 여부
    'TRADING_INTERVAL': 1,    # 매매 간격 (분)
    'MAX_COINS': 5,           # 동시 보유 가능한 최대 코인 수
    'RISK_LEVEL': 'MEDIUM'    # 위험도 (LOW, MEDIUM, HIGH)
}

# 위험도별 설정
RISK_SETTINGS = {
    'LOW': {
        'STOP_LOSS': 2.0,
        'TAKE_PROFIT': 3.0,
        'MAX_AMOUNT_RATIO': 0.3  # 보유 금액의 최대 30%까지 투자
    },
    'MEDIUM': {
        'STOP_LOSS': 3.0,
        'TAKE_PROFIT': 5.0,
        'MAX_AMOUNT_RATIO': 0.5  # 보유 금액의 최대 50%까지 투자
    },
    'HIGH': {
        'STOP_LOSS': 5.0,
        'TAKE_PROFIT': 8.0,
        'MAX_AMOUNT_RATIO': 0.8  # 보유 금액의 최대 80%까지 투자
    }
} 