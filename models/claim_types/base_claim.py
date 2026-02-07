from abc import ABC, abstractmethod

class Claim(ABC):
    def __init__(self, monthly_income: float, cap: float):
        self.monthly_income = monthly_income
        self.cap = cap

    @abstractmethod
    def calculate(self) -> float:
        ...
