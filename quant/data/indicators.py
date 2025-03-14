import pandas as pd

class Indicators:
    @staticmethod
    def sma(data: pd.DataFrame, window: int) -> pd.Series:
        """计算简单移动平均线"""
        return data['close'].rolling(window=window).mean()

    @staticmethod
    def ema(data: pd.DataFrame, window: int) -> pd.Series:
        """计算指数移动平均线"""
        return data['close'].ewm(span=window, adjust=False).mean()

    def calculate(self, data: pd.DataFrame, indicators: dict) -> pd.DataFrame:
        """批量计算指标"""
        result = data.copy()
        for name, params in indicators.items():
            if name == 'sma':
                result[f'sma_{params["window"]}'] = self.sma(data, params['window'])
            elif name == 'ema':
                result[f'ema_{params["window"]}'] = self.ema(data, params['window'])
        return result

# 示例
if __name__ == "__main__":
    df = pd.DataFrame({
        'close': [100, 101, 102, 103, 104],
    })
    indicators = Indicators()
    result = indicators.calculate(df, {'sma': {'window': 3}, 'ema': {'window': 3}})
    print(result)