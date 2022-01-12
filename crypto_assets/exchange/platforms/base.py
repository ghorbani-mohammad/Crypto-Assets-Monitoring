from abc import ABC, abstractmethod


class BaseExchange(ABC):
    @abstractmethod
    def get_price(self, coin) -> int:
        pass
