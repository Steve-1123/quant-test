from dataclasses import dataclass
from typing import List
import pandas as pd

@dataclass
class Trade:
    timestamp: str
    action: str
    price: float
    quantity: float

class TradeLog:
    def __init__(self):
        self.trades: List[Trade] = []

    def add_trade(self, timestamp: str, action: str, price: float, quantity: float) -> None:
        trade = Trade(timestamp, action, price, quantity)
        self.trades.append(trade)

    def to_df(self) -> 'pd.DataFrame':
        return pd.DataFrame([vars(t) for t in self.trades])