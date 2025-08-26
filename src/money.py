from decimal import Decimal, ROUND_HALF_UP, getcontext
from dataclasses import dataclass

getcontext().prec = 28

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "CAD"

    @staticmethod
    def parse(text: str, currency: str = "CAD") -> "Money":
        # Allows "12.34" style input
        return Money(Decimal(text).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), currency)

    def __add__(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money((self.amount + other.amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money((self.amount - other.amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), self.currency)

    def gte(self, other: "Money") -> bool:
        self._ensure_same_currency(other)
        return self.amount >= other.amount

    def lt(self, other: "Money") -> bool:
        self._ensure_same_currency(other)
        return self.amount < other.amount

    def _ensure_same_currency(self, other: "Money"):
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"
