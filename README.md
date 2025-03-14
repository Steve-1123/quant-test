# quant-test

test project for quantitative exchange (test first push)

## Project Structure

```text
quant-test/
├── config                    # config for different enviroments.
│   ├── .env                  # Configuration Variables (not been tracked by git)
│   └── config.py             # Configuration Classed for different environments
├── data_process_biz          # Process data before trading
│   └── data_process_biz.py   
├── quant_demo
│   └── quant_demo.py
├── strategy_biz              # Trading strategy (contains several kinds of trading strategy)
├── README.md                 # Project documentation (this file)
├── app.py                    # Main Flask application entry point
└── requirements.txt          # Python dependencies
```

## Requirements

The project is built with Python 3.8+ and requires the following dependencies:

```text
ccxt==4.4.64
Flask==3.1.0
pandas==2.2.3
pipdeptree==2.25.1
```

See `requirements.txt` for the full list.

```shell
pip install -r requirements.txt
```

## Configuration

Environment Variables
The project uses a .env file to manage sensitive configurations. Create a .env file in the root directory with the following structure:

```text
# .env
FLASK_ENV=development       # Options: development, production, testing
SECRET_KEY=your-secret-key  # A random string for Flask security
API_KEY=your-api-key        # Trading API key (e.g., Longbridge, Binance)
API_SECRET=your-api-secret  # Trading API secret
DATABASE_URL=sqlite:///trading.db  # Database URI (optional)
```
