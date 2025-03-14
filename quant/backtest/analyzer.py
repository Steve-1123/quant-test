import pandas as pd
from quant.backtest.trade_log import TradeLog

class PerformanceAnalyzer:
    def __init__(self, trade_log: TradeLog, initial_cash: float, final_value: float):
        self.trade_log = trade_log
        self.initial_cash = initial_cash
        self.final_value = final_value

    def calculate_metrics(self) -> dict:
        """计算关键绩效指标"""
        trades_df = self.trade_log.to_df()
        total_return = (self.final_value - self.initial_cash) / self.initial_cash
        
        # 计算胜率
        if len(trades_df) > 0:
            wins = trades_df[trades_df['action'] == 'SELL']['price'].diff().gt(0).sum()
            win_rate = wins / len(trades_df) if len(trades_df) > 0 else 0
        else:
            win_rate = 0
        
        return {
            'total_return': total_return,
            'win_rate': win_rate,
            'trade_count': len(trades_df)
        }

# 示例
if __name__ == "__main__":
    log = TradeLog()
    log.add_trade('2023-01-01', 'BUY', 100, 10)
    log.add_trade('2023-01-02', 'SELL', 110, 10)
    analyzer = PerformanceAnalyzer(log, 10000, 10100)
    print(analyzer.calculate_metrics())