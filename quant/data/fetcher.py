import requests
import time
from typing import Dict, Any
from conf import Config

class DataFetcher:
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.base_url = Config.DATA_API_URL  # 如 "https://api.example.com"
        self.api_key = api_key or Config.API_KEY
        self.headers = {'Authorization': f'Bearer {self.api_key}'}

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100, retries: int = 3) -> Dict[str, Any]:
        """获取OHLCV数据"""
        url = f"{self.base_url}/ohlcv"
        params = {'symbol': symbol, 'timeframe': timeframe, 'limit': limit}
        
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Fetch failed (attempt {attempt + 1}/{retries}): {e}")
                time.sleep(2 ** attempt)  # 指数退避
        raise Exception(f"Failed to fetch data after {retries} attempts")

# 示例配置
if __name__ == "__main__":
    fetcher = DataFetcher()
    data = fetcher.fetch_ohlcv('BTC/USDT', '1h')
    print(data)