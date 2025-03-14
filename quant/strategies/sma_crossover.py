import pandas as pd

def sma_crossover(data: pd.DataFrame) -> str:
    """双均线交叉策略"""
    if 'sma_10' not in data.columns or 'sma_30' not in data.columns:
        raise ValueError("Data must contain 'sma_10' and 'sma_30' columns")
    
    short_sma = data['sma_10']
    long_sma = data['sma_30']
    
    if (short_sma.iloc[-1] > long_sma.iloc[-1] and 
        short_sma.iloc[-2] <= long_sma.iloc[-2]):
        return 'BUY'
    elif (short_sma.iloc[-1] < long_sma.iloc[-1] and 
          short_sma.iloc[-2] >= long_sma.iloc[-2]):
        return 'SELL'
    return 'HOLD'

# 示例
if __name__ == "__main__":
    df = pd.DataFrame({
        'close': [100, 101, 102, 103, 104],
        'sma_10': [101, 101.5, 102, 102.5, 103],
        'sma_30': [102, 102, 102, 102, 102]
    })
    signal = sma_crossover(df)
    print(f"Signal: {signal}")