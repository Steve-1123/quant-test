from typing import Callable, List
import pandas as pd
from quant.data.processor import DataProcessor
from quant.data.indicators import Indicators
from quant.backtest.trade_log import TradeLog

class BacktestEngine:
    def __init__(self, initial_cash: float = 10000.0, commission: float = 0.001):
        self.cash = initial_cash
        self.initial_cash = initial_cash
        self.commission = commission  # 交易手续费率
        self.position = 0  # 持仓数量
        self.trade_log = TradeLog()
        self.processor = DataProcessor()
        self.indicators = Indicators()

    def run(self, data: pd.DataFrame, strategy: Callable[[pd.DataFrame], str], quantity: float = 100) -> None:
        """运行回测"""
        # 计算指标（假设策略需要SMA）
        data_with_indicators = self.indicators.calculate(data, {
            'sma': {'window': 10},
            'sma': {'window': 30}
        })

        for index, row in data_with_indicators.iterrows():
            signal = strategy(row)  # 调用策略生成信号
            
            if signal == 'BUY' and self.cash >= row['close'] * quantity:
                cost = row['close'] * quantity * (1 + self.commission)
                self.cash -= cost
                self.position += quantity
                self.trade_log.add_trade(index, 'BUY', row['close'], quantity)
            
            elif signal == 'SELL' and self.position >= quantity:
                revenue = row['close'] * quantity * (1 - self.commission)
                self.cash += revenue
                self.position -= quantity
                self.trade_log.add_trade(index, 'SELL', row['close'], quantity)

    def get_results(self) -> dict:
        """返回回测结果"""
        final_value = self.cash + self.position * self.trade_log.trades[-1]['price'] if self.position > 0 else self.cash
        return {
            'initial_cash': self.initial_cash,
            'final_value': final_value,
            'total_return': (final_value - self.initial_cash) / self.initial_cash,
            'trades': self.trade_log.trades
        }

# 示例
if __name__ == "__main__":
    from strategies.sma_crossover import sma_crossover
    df = pd.DataFrame({
        'timestamp': pd.date_range('2023-01-01', periods=50, freq='H'),
        'close': [100 + i * 0.5 for i in range(50)]
    }).set_index('timestamp')
    
    engine = BacktestEngine()
    engine.run(df, sma_crossover)
    print(engine.get_results())