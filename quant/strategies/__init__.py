# strategies/__init__.py
from .sma_crossover import sma_crossover
from .mean_reversion import mean_reversion

# 策略映射（便于app.py动态调用）
STRATEGIES = {
    'sma_crossover': sma_crossover,
    'mean_reversion': mean_reversion
}

__all__ = ['sma_crossover', 'mean_reversion', 'STRATEGIES']