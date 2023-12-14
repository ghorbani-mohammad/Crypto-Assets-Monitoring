from abc import ABC, abstractmethod
from decimal import Decimal


class BaseExchange(ABC):
    @abstractmethod
    def get_price(self, coin, market: str) -> Decimal:
        pass

    @abstractmethod
    def cache_all_prices(self) -> None:
        pass
