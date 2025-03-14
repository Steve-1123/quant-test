# Quant Trading System

A Flask-based quantitative trading system designed for automating trading strategies using market data. This project supports real-time trading and backtesting with extensible modules for data processing, strategy execution, and performance analysis.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Program](#running-the-program)
  - [Real-Time Trading](#real-time-trading)
  - [Backtesting](#backtesting)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project implements a modular quantitative trading system with the following components:

- **Data Processing**: Fetches and processes market data (e.g., OHLCV).
- **Strategies**: Implements trading strategies like SMA crossover and mean reversion.
- **Execution**: Simulates or executes trades via a trading API.
- **Backtesting**: Evaluates strategy performance using historical data.

The system runs as a Flask web service, providing endpoints for trading and backtesting.

## Project Structure

```text
quant-trading/
├── data/                  # Data processing module
│   ├── __init__.py
│   ├── fetcher.py         # Fetches market data
│   ├── processor.py       # Cleans and formats data
│   └── indicators.py      # Calculates technical indicators
├── strategies/            # Trading strategies module
│   ├── __init__.py
│   ├── sma_crossover.py   # SMA crossover strategy
│   └── mean_reversion.py  # Mean reversion strategy
├── execution/             # Trade execution module
│   ├── __init__.py
│   └── trader.py          # Executes trades (simulated or real)
├── backtest/              # Backtesting module
│   ├── __init__.py
│   ├── engine.py          # Backtest engine
│   ├── trade_log.py       # Logs trades
│   └── analyzer.py        # Analyzes performance
├── app.py                 # Flask service entry point
├── config.py              # Configuration management
├── .env                   # Environment variables (not tracked)
├── .gitignore             # Git ignore file
└── requirements.txt       # Python dependencies
```

## Features

- **Real-Time Trading**: Execute trades based on strategy signals via a simulated or real trading API.
- **Backtesting**: Test strategies on historical data with performance metrics (e.g., total return, win rate).
- **Modular Design**: Easily extend with new strategies, data sources, or execution methods.
- **Web Interface**: Access trading and backtesting via Flask API endpoints.

## Requirements

The project requires Python 3.8+ and the following dependencies:

```text
Flask==2.3.3
pandas==2.1.0
requests==2.31.0
python-dotenv==1.0.0
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Steve-1123/quant-test.git
   cd quant-trading
   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The project uses environment variables stored in a `.env` file for configuration.

1. **Create a `.env` file** in the project root:

   ```text
   # .env
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-123
   DATA_API_URL=https://api.example.com
   TRADING_API_URL=https://trade.example.com
   API_KEY=your-api-key
   API_SECRET=your-api-secret
   DEBUG=True
   ```

2. **Notes**:
   - Replace `DATA_API_URL` and `TRADING_API_URL` with actual API endpoints (e.g., Binance: `https://api.binance.com`).
   - Use valid `API_KEY` and `API_SECRET` for your trading platform.
   - `.env` is ignored by Git (listed in `.gitignore`) to protect sensitive data.

## Running the Program

### Real-Time Trading

1. **Start the Flask service**:

   ```bash
   python app.py
   ```

   - The service will run on `http://localhost:5000`.

2. **Access trading endpoint**:
   - Use a browser or `curl` to trigger a trade:

     ```bash
     curl http://localhost:5000/trade/BTC-USDT/sma_crossover
     ```

   - Available strategies: `sma_crossover`, `mean_reversion`.
   - Response example:

     ```json
     {"signal": "BUY", "trade": {"trade_id": "sim-123", "symbol": "BTC-USDT", "quantity": 100, "side": "BUY", "price": 100.0, "status": "filled"}}
     ```

3. **Switch to real trading** (optional):
   - Edit `app.py`, set `trader = Trader(simulate=False)` and ensure API credentials are valid.

### Backtesting

1. **Run a backtest**:
   - Use the backtest endpoint:

     ```bash
     curl http://localhost:5000/backtest/BTC-USDT/sma_crossover
     ```

   - Response example:

     ```json
     {
       "results": {"initial_cash": 10000.0, "final_value": 10500.0, "total_return": 0.05, "trades": [...]},
       "metrics": {"total_return": 0.05, "win_rate": 0.6, "trade_count": 10}
     }
     ```

2. **Customize backtest**:
   - Modify `backtest/engine.py` to adjust initial cash, commission, or quantity.

### Notes

- Ensure your data source (`DATA_API_URL`) returns valid OHLCV data in JSON format.
- For real trading, replace the simulated price in `execution/trader.py` with actual API calls.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
