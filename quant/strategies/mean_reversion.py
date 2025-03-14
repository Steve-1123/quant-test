import pandas as pd

def mean_reversion(data: pd.DataFrame, window: int = 20, threshold: float = 1.0) -> str:
    """均值回归策略"""
    if 'close' not in data.columns:
        raise ValueError("Data must contain 'close' column")
    
    mean = data['close'].rolling(window=window).mean()
    std = data['close'].rolling(window=window).std()
    
    current_price = data['close'].iloc[-1]
    current_mean = mean.iloc[-1]
    current_std = std.iloc[-1]
    
    if current_price < current_mean - threshold * current_std:
        return 'BUY'  # 价格低于均值一个标准差，买入
    elif current_price > current_mean + threshold * current_std:
        return 'SELL'  # 价格高于均值一个标准差，卖出
    return 'HOLD'

# 示例
if __name__ == "__main__":
    df = pd.DataFrame({
        'close': [100, 98, 95, 102, 105]
    })
    signal = mean_reversion(df)
    print(f"Signal: {signal}")