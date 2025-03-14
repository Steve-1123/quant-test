from flask import Flask, jsonify
from quant.data import DataFetcher, DataProcessor, Indicators
from quant.strategies import sma_crossover, mean_reversion, STRATEGIES
from quant.execution import Trader
from quant.backtest import BacktestEngine, PerformanceAnalyzer
from conf import DevelopmentConfig, ProductionConfig, TestingConfig
import os

# 初始化Flask应用
app = Flask(__name__)

# 根据环境加载配置
env = os.getenv('FLASK_ENV', 'development')
if env == 'development':
    app.config.from_object(DevelopmentConfig)
elif env == 'production':
    app.config.from_object(ProductionConfig)
elif env == 'testing':
    app.config.from_object(TestingConfig)

# 初始化模块实例
fetcher = DataFetcher()
processor = DataProcessor()
indicators = Indicators()
trader = Trader(simulate=True)  # 默认模拟交易

# API端点

@app.route('/')
def home():
    """欢迎页面"""
    return jsonify({"message": "Welcome to Quant Trading System", "env": env})

@app.route('/trade/<symbol>/<strategy_name>')
def trade(symbol, strategy_name):
    """实时交易端点"""
    if strategy_name not in STRATEGIES:
        return jsonify({"error": "Invalid strategy"}), 400
    
    # 获取和处理数据
    raw_data = fetcher.fetch_ohlcv(symbol, '1h', limit=100)
    processed_data = processor.process(raw_data)
    data_with_indicators = indicators.calculate(processed_data, {
        'sma': {'window': 10},
        'sma': {'window': 30}
    })
    
    # 调用策略
    strategy = STRATEGIES[strategy_name]
    signal = strategy(data_with_indicators)
    
    # 执行交易
    if signal in ['BUY', 'SELL']:
        trade_result = trader.execute_trade(symbol, 100, signal)
        return jsonify({'signal': signal, 'trade': trade_result})
    return jsonify({'signal': signal, 'trade': None})

@app.route('/backtest/<symbol>/<strategy_name>')
def backtest(symbol, strategy_name):
    """回测端点"""
    if strategy_name not in STRATEGIES:
        return jsonify({"error": "Invalid strategy"}), 400
    
    # 获取历史数据
    raw_data = fetcher.fetch_ohlcv(symbol, '1h', limit=1000)
    processed_data = processor.process(raw_data)
    
    # 运行回测
    engine = BacktestEngine(initial_cash=10000.0)
    strategy = STRATEGIES[strategy_name]
    engine.run(processed_data, strategy)
    results = engine.get_results()
    
    # 分析绩效
    analyzer = PerformanceAnalyzer(engine.trade_log, results['initial_cash'], results['final_value'])
    metrics = analyzer.calculate_metrics()
    
    return jsonify({'results': results, 'metrics': metrics})

# 启动服务
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])

