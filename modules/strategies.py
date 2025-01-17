from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import random

class TradingStrategy(ABC):
    @abstractmethod
    def should_buy(self, data) -> bool:
        pass
        
    @abstractmethod
    def should_sell(self, data) -> bool:
        pass

class RSIStrategy(TradingStrategy):
    def __init__(self, period=14, oversold=30, overbought=70):
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        
    def calculate_rsi(self, data):
        df = pd.DataFrame(data)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
        
    def should_buy(self, data):
        rsi = self.calculate_rsi(data)
        return rsi.iloc[-1] < self.oversold
        
    def should_sell(self, data):
        rsi = self.calculate_rsi(data)
        return rsi.iloc[-1] > self.overbought

class MACDStrategy(TradingStrategy):
    def __init__(self, fast=12, slow=26, signal=9):
        self.fast = fast
        self.slow = slow
        self.signal = signal
        
    def calculate_macd(self, data):
        df = pd.DataFrame(data)
        exp1 = df['close'].ewm(span=self.fast).mean()
        exp2 = df['close'].ewm(span=self.slow).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=self.signal).mean()
        return macd, signal
        
    def should_buy(self, data):
        macd, signal = self.calculate_macd(data)
        return macd.iloc[-1] > signal.iloc[-1]
        
    def should_sell(self, data):
        macd, signal = self.calculate_macd(data)
        return macd.iloc[-1] < signal.iloc[-1]

class BollingerBandsStrategy(TradingStrategy):
    def __init__(self, period=20, std_dev=2):
        self.period = period
        self.std_dev = std_dev
        
    def calculate_bands(self, data):
        df = pd.DataFrame(data)
        ma = df['close'].rolling(window=self.period).mean()
        std = df['close'].rolling(window=self.period).std()
        upper = ma + (std * self.std_dev)
        lower = ma - (std * self.std_dev)
        return upper, ma, lower
        
    def should_buy(self, data):
        upper, ma, lower = self.calculate_bands(data)
        return data['close'].iloc[-1] < lower.iloc[-1]
        
    def should_sell(self, data):
        upper, ma, lower = self.calculate_bands(data)
        return data['close'].iloc[-1] > upper.iloc[-1]

class StochasticStrategy(TradingStrategy):
    def __init__(self, k_period=14, d_period=3):
        self.k_period = k_period
        self.d_period = d_period
        
    def calculate_stoch(self, data):
        low_min = data['low'].rolling(window=self.k_period).min()
        high_max = data['high'].rolling(window=self.k_period).max()
        k = 100 * (data['close'] - low_min) / (high_max - low_min)
        d = k.rolling(window=self.d_period).mean()
        return k, d
        
    def should_buy(self, data):
        k, d = self.calculate_stoch(data)
        return k.iloc[-1] < 20 and k.iloc[-1] > d.iloc[-1]
        
    def should_sell(self, data):
        k, d = self.calculate_stoch(data)
        return k.iloc[-1] > 80 and k.iloc[-1] < d.iloc[-1]

class AIStrategy:
    def __init__(self):
        self.learning_data = []
        
    def add_learning_data(self, data):
        self.learning_data.append(data)
        
    def clear_learning_data(self):
        self.learning_data = []

class AIBasicStrategy(AIStrategy):
    def __init__(self):
        super().__init__()
        
    def analyze_data(self, data):
        df = pd.DataFrame(data)
        # 기본적인 기술적 지표 계산
        df['rsi'] = self.calculate_rsi(df['close'])
        df['macd'], df['signal'] = self.calculate_macd(df['close'])
        df['upper'], df['middle'], df['lower'] = self.calculate_bollinger(df['close'])
        return df
        
    def calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
        
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        exp1 = prices.ewm(span=fast).mean()
        exp2 = prices.ewm(span=slow).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal).mean()
        return macd, signal_line
        
    def calculate_bollinger(self, prices, period=20, std=2):
        middle = prices.rolling(window=period).mean()
        std_dev = prices.rolling(window=period).std()
        upper = middle + (std_dev * std)
        lower = middle - (std_dev * std)
        return upper, middle, lower
        
    def should_buy(self, data):
        df = self.analyze_data(data)
        
        # 매수 신호 조합
        rsi_buy = df['rsi'].iloc[-1] < 30
        macd_buy = df['macd'].iloc[-1] > df['signal'].iloc[-1]
        bb_buy = df['close'].iloc[-1] < df['lower'].iloc[-1]
        
        # 매수 조건: RSI 과매도 + MACD 상향돌파 또는 볼린저밴드 하단 돌파
        return (rsi_buy and macd_buy) or bb_buy
        
    def should_sell(self, data):
        df = self.analyze_data(data)
        
        # 매도 신호 조합
        rsi_sell = df['rsi'].iloc[-1] > 70
        macd_sell = df['macd'].iloc[-1] < df['signal'].iloc[-1]
        bb_sell = df['close'].iloc[-1] > df['upper'].iloc[-1]
        
        # 매도 조건: RSI 과매수 + MACD 하향돌파 또는 볼린저밴드 상단 돌파
        return (rsi_sell and macd_sell) or bb_sell

class AIAdvancedStrategy(AIStrategy):
    def __init__(self):
        super().__init__()
        self.min_samples = 100
        
    def analyze_data(self, data):
        df = super().analyze_data(data)
        # 추가 지표 계산
        df['vwap'] = self.calculate_vwap(df)
        df['atr'] = self.calculate_atr(df)
        df['trend'] = self.calculate_trend(df)
        return df
        
    def calculate_vwap(self, df, period=14):
        return (df['close'] * df['volume']).rolling(window=period).sum() / df['volume'].rolling(window=period).sum()
        
    def calculate_atr(self, df, period=14):
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(window=period).mean()
        
    def calculate_trend(self, df, period=20):
        return df['close'].rolling(window=period).mean().diff()
        
    def should_buy(self, data):
        df = self.analyze_data(data)
        
        # 기본 전략의 신호
        basic_buy = super().should_buy(data)
        
        # 추가 매수 신호
        vwap_buy = df['close'].iloc[-1] < df['vwap'].iloc[-1]
        trend_buy = df['trend'].iloc[-1] > 0
        volume_buy = df['volume'].iloc[-1] > df['volume'].rolling(window=20).mean().iloc[-1]
        
        # 매수 조건: 기본 전략 + 추가 조건들
        return basic_buy and (vwap_buy or (trend_buy and volume_buy))
        
    def should_sell(self, data):
        df = self.analyze_data(data)
        
        # 기본 전략의 신호
        basic_sell = super().should_sell(data)
        
        # 추가 매도 신호
        vwap_sell = df['close'].iloc[-1] > df['vwap'].iloc[-1]
        trend_sell = df['trend'].iloc[-1] < 0
        volume_sell = df['volume'].iloc[-1] < df['volume'].rolling(window=20).mean().iloc[-1]
        
        # 매도 조건: 기본 전략 + 추가 조건들
        return basic_sell and (vwap_sell or (trend_sell and volume_sell))

class AIFullStrategy(AIStrategy):
    def __init__(self):
        super().__init__()
        self.min_samples = 200
        self.max_memory = 1000
        self.confidence_threshold = 0.7
        
    def analyze_data(self, data):
        df = super().analyze_data(data)
        # 추가 고급 지표 계산
        df['volatility'] = self.calculate_volatility(df)
        df['momentum'] = self.calculate_momentum(df)
        df['market_phase'] = self.identify_market_phase(df)
        return df
        
    def calculate_volatility(self, df, period=20):
        return df['close'].pct_change().rolling(window=period).std()
        
    def calculate_momentum(self, df, period=14):
        return df['close'].diff(period) / df['close'].shift(period) * 100
        
    def identify_market_phase(self, df, period=20):
        sma = df['close'].rolling(window=period).mean()
        std = df['close'].rolling(window=period).std()
        z_score = (df['close'] - sma) / std
        return pd.cut(z_score, bins=[-np.inf, -2, -0.5, 0.5, 2, np.inf], 
                     labels=['Strong Bear', 'Bear', 'Neutral', 'Bull', 'Strong Bull'])
        
    def should_buy(self, data):
        df = self.analyze_data(data)
        
        # 고급 전략의 신호
        advanced_buy = super().should_buy(data)
        
        # 추가 매수 신호
        volatility_ok = df['volatility'].iloc[-1] < df['volatility'].rolling(window=100).mean().iloc[-1]
        momentum_buy = df['momentum'].iloc[-1] > 0
        market_phase_buy = df['market_phase'].iloc[-1] in ['Bull', 'Strong Bull']
        
        # 매수 신호 신뢰도 계산
        buy_signals = [advanced_buy, volatility_ok, momentum_buy, market_phase_buy]
        confidence = sum(buy_signals) / len(buy_signals)
        
        # 매수 조건: 신뢰도가 임계값을 넘을 때
        return confidence > self.confidence_threshold
        
    def should_sell(self, data):
        df = self.analyze_data(data)
        
        # 고급 전략의 신호
        advanced_sell = super().should_sell(data)
        
        # 추가 매도 신호
        volatility_high = df['volatility'].iloc[-1] > df['volatility'].rolling(window=100).mean().iloc[-1]
        momentum_sell = df['momentum'].iloc[-1] < 0
        market_phase_sell = df['market_phase'].iloc[-1] in ['Bear', 'Strong Bear']
        
        # 매도 신호 신뢰도 계산
        sell_signals = [advanced_sell, volatility_high, momentum_sell, market_phase_sell]
        confidence = sum(sell_signals) / len(sell_signals)
        
        # 매도 조건: 신뢰도가 임계값을 넘을 때
        return confidence > self.confidence_threshold

class SMAStrategy(TradingStrategy):
    def __init__(self, short_period=5, long_period=20):
        self.short_period = short_period
        self.long_period = long_period
        
    def should_buy(self, data):
        df = pd.DataFrame(data)
        short_ma = df['close'].rolling(window=self.short_period).mean()
        long_ma = df['close'].rolling(window=self.long_period).mean()
        return short_ma.iloc[-1] > long_ma.iloc[-1]
        
    def should_sell(self, data):
        df = pd.DataFrame(data)
        short_ma = df['close'].rolling(window=self.short_period).mean()
        long_ma = df['close'].rolling(window=self.long_period).mean()
        return short_ma.iloc[-1] < long_ma.iloc[-1]

class StochasticStrategy(TradingStrategy):
    def __init__(self, k_period=14, d_period=3):
        self.k_period = k_period
        self.d_period = d_period
        
    def should_buy(self, data):
        # 구현 필요
        return False
        
    def should_sell(self, data):
        # 구현 필요
        return False 

class VWAPStrategy(TradingStrategy):
    def __init__(self, period=14):
        self.period = period
        
    def calculate_vwap(self, data):
        df = pd.DataFrame(data)
        df['vwap'] = (df['close'] * df['volume']).rolling(window=self.period).sum() / df['volume'].rolling(window=self.period).sum()
        return df['vwap']
        
    def should_buy(self, data):
        vwap = self.calculate_vwap(data)
        return data['close'].iloc[-1] < vwap.iloc[-1]
        
    def should_sell(self, data):
        vwap = self.calculate_vwap(data)
        return data['close'].iloc[-1] > vwap.iloc[-1]

class IchimokuStrategy(TradingStrategy):
    def should_buy(self, data):
        return False  # 구현 필요
        
    def should_sell(self, data):
        return False  # 구현 필요

class SuperTrendStrategy(TradingStrategy):
    def should_buy(self, data):
        return False  # 구현 필요
        
    def should_sell(self, data):
        return False  # 구현 필요

class DMIStrategy(TradingStrategy):
    def should_buy(self, data):
        return False  # 구현 필요
        
    def should_sell(self, data):
        return False  # 구현 필요

class WilliamsStrategy(TradingStrategy):
    def should_buy(self, data):
        return False  # 구현 필요
        
    def should_sell(self, data):
        return False  # 구현 필요

class TrendFollowStrategy(TradingStrategy):
    def should_buy(self, data):
        return False  # 구현 필요
        
    def should_sell(self, data):
        return False  # 구현 필요

class VolBreakoutStrategy(TradingStrategy):
    def should_buy(self, data):
        return False  # 구현 필요
        
    def should_sell(self, data):
        return False  # 구현 필요

class MultiMAStrategy(TradingStrategy):
    def should_buy(self, data):
        return False  # 구현 필요
        
    def should_sell(self, data):
        return False  # 구현 필요

class MomentumRevStrategy(TradingStrategy):
    def should_buy(self, data):
        return False  # 구현 필요
        
    def should_sell(self, data):
        return False  # 구현 필요

class VolumeBreakStrategy(TradingStrategy):
    def should_buy(self, data):
        return False  # 구현 필요
        
    def should_sell(self, data):
        return False  # 구현 필요 