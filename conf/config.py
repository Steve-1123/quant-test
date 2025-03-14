# conf/config.py
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DATA_API_URL = os.getenv('DATA_API_URL', 'https://api.example.com')
    TRADING_API_URL = os.getenv('TRADING_API_URL', 'https://trade.example.com')
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')

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

