import pandas as pd
from typing import Dict, Any

class DataProcessor:
    def process(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """清洗和格式化数据"""
        df = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # 处理缺失值
        df = df.dropna()
        
        # 检查异常值（简单示例）
        df = df[df['close'] > 0]
        
        return df.set_index('timestamp')

# 示例
if __name__ == "__main__":
    raw_data = {
        'timestamp': [1609459200000, 1609462800000],
        'open': [29000, 29200],
        'high': [29500, 29600],
        'low': [28900, 29100],
        'close': [29400, 29500],
        'volume': [100, 150]
    }
    processor = DataProcessor()
    df = processor.process(raw_data)
    print(df)