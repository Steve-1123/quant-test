# conf/config.py
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class OKXConfig:
    SECRET_KEY = os.getenv('OKX_SECRET_KEY', 'default-secret-key')
    API_KEY = os.getenv('OKX_API_KEY')
    PASSPHRASE = os.getenv('OKX_PASSPHRASE')
    FLAG=os.getenv('OKX_SIMULATED_FLAG')

class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    DATA_API_URL = os.getenv('DATA_API_URL', 'https://api.example.com')
    TRADING_API_URL = os.getenv('TRADING_API_URL', 'https://trade.example.com')

    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    API_KEY = os.getenv('API_KEY')
    PASSPHRASE = os.getenv('PASSPHRASE')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

def get_config():
    """根据 FLASK_ENV 返回对应的配置类"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    # 返回匹配的配置类实例，如果 env 无效则默认 DevelopmentConfig
    return config_map.get(env, DevelopmentConfig)()

