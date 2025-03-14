import requests
import time
from typing import Optional
from config import Config

class Trader:
    def __init__(self, api_key: str = None, api_secret: str = None, simulate: bool = True):
        self.api_key = api_key or Config.API_KEY
        self.api_secret = api_secret or Config.API_SECRET
        self.base_url = Config.TRADING_API_URL  # 如 "https://api.example.com"
        self.headers = {'Authorization': f'Bearer {self.api_key}'}
        self.simulate = simulate  # True为模拟交易，False为真实交易

    def execute_trade(self, symbol: str, quantity: float, side: str) -> dict:
        """执行交易订单"""
        if self.simulate:
            return self._simulate_trade(symbol, quantity, side)
        else:
            return self._real_trade(symbol, quantity, side)

    def _simulate_trade(self, symbol: str, quantity: float, side: str) -> dict:
        """模拟交易"""
        trade_id = f"sim-{int(time.time())}"
        price = self._get_current_price(symbol)  # 模拟获取当前价格
        return {
            'trade_id': trade_id,
            'symbol': symbol,
            'quantity': quantity,
            'side': side,
            'price': price,
            'status': 'filled'
        }

    def _real_trade(self, symbol: str, quantity: float, side: str) -> dict:
        """真实交易"""
        url = f"{self.base_url}/order"
        payload = {
            'symbol': symbol,
            'quantity': quantity,
            'side': side.lower(),
            'order_type': 'market'
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'status': 'error', 'message': str(e)}

    def _get_current_price(self, symbol: str) -> float:
        """获取当前价格（模拟或真实）"""
        # 这里可以调用data.fetcher获取实时价格
        return 100.0  # 模拟价格，实际应替换为API调用

# 示例
if __name__ == "__main__":
    trader = Trader(simulate=True)
    result = trader.execute_trade('BTC/USDT', 0.1, 'BUY')
    print(result)