# app.py
import os
from flask import Flask, jsonify
from conf.config import get_config
from quant.data import DataFetcher, DataProcessor, Indicators
from quant.strategies import STRATEGIES
from quant.execution import Trader
from quant.backtest import BacktestEngine, PerformanceAnalyzer

from quant.utils.okx_http_client import OKXHttpClient

app = Flask(__name__)
app.config.from_object(get_config())  # 直接加载配置

fetcher = DataFetcher()
processor = DataProcessor()
indicators = Indicators()
trader = Trader(simulate=True)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Quant Trading System"})

@app.route('/trade/<symbol>/<strategy_name>')
def trade(symbol, strategy_name):
    strategy = STRATEGIES.get(strategy_name)
    if not strategy:
        return jsonify({"error": "Invalid strategy"}), 400
    raw_data = fetcher.fetch_ohlcv(symbol, '1h', limit=100)
    processed_data = processor.process(raw_data)
    data_with_indicators = indicators.calculate(processed_data, {'sma': {'window': 10}, 'sma': {'window': 30}})
    signal = strategy(data_with_indicators)
    if signal in ['BUY', 'SELL']:
        trade_result = trader.execute_trade(symbol, 100, signal)
        return jsonify({'signal': signal, 'trade': trade_result})
    return jsonify({'signal': signal, 'trade': None})

@app.route('/backtest/<symbol>/<strategy_name>')
def backtest(symbol, strategy_name):
    strategy = STRATEGIES.get(strategy_name)
    if not strategy:
        return jsonify({"error": "Invalid strategy"}), 400
    raw_data = fetcher.fetch_ohlcv(symbol, '1h', limit=1000)
    processed_data = processor.process(raw_data)
    engine = BacktestEngine(initial_cash=10000.0)
    engine.run(processed_data, strategy)
    results = engine.get_results()
    analyzer = PerformanceAnalyzer(engine.trade_log, results['initial_cash'], results['final_value'])
    metrics = analyzer.calculate_metrics()
    return jsonify({'results': results, 'metrics': metrics})

@app.route('/test_api')
def test_api():
    okx_client = OKXHttpClient('1')
    resp = okx_client.get_account()
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=app.config['DEBUG'])

