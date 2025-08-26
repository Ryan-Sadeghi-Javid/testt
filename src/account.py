from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Tuple
from .money import Money
from .errors import InsufficientFunds, InvalidOperation

Transaction = Tuple[str, Money]  # simple: ("DEPOSIT"|"WITHDRAW"|"TRANSFER_IN"|"TRANSFER_OUT", amount)

@dataclass
class Account(ABC):
    id: str
    holder: str
    balance: Money
    _history: List[Transaction] = field(default_factory=list)

    def deposit(self, amount: Money):
        if amount.amount <= 0:
            raise InvalidOperation("Deposit must be positive")
        self.balance = self.balance + amount
        self._history.append(("DEPOSIT", amount))

    def withdraw(self, amount: Money):
        if amount.amount <= 0:
            raise InvalidOperation("Withdraw must be positive")
        if not self._can_withdraw(amount):
            raise InsufficientFunds("Insufficient funds")
        self.balance = self.balance - amount
        self._history.append(("WITHDRAW", amount))

    def transfer_out(self, amount: Money):
        if not self._can_withdraw(amount):
            raise InsufficientFunds("Insufficient funds for transfer")
        self.balance = self.balance - amount
        self._history.append(("TRANSFER_OUT", amount))

    def transfer_in(self, amount: Money):
        self.balance = self.balance + amount
        self._history.append(("TRANSFER_IN", amount))

    def statement(self) -> str:
        lines = [f"Account {self.id} ({self.holder}) - Balance: {self.balance}"]
        for kind, amt in self._history:
            lines.append(f"{kind:<12} {amt}")
        return "\n".join(lines)

    @abstractmethod
    def _can_withdraw(self, amount: Money) -> bool:
        ...

@dataclass
class CheckingAccount(Account):
    overdraft_limit: Money | None = None

    def _can_withdraw(self, amount: Money) -> bool:
        if self.overdraft_limit is None:
            return self.balance.gte(amount)
        remaining = (self.balance.amount - amount.amount)
        return remaining >= -self.overdraft_limit.amount

@dataclass
class SavingsAccount(Account):
    annual_interest_rate_bps: int = 150  # 1.50% default

    def _can_withdraw(self, amount: Money) -> bool:
        return self.balance.gte(amount)

    def apply_monthly_interest(self):
        # naive monthly compounding: rate/12
        monthly_rate = self.annual_interest_rate_bps / 10000 / 12
        incr = Money(self.balance.amount * monthly_rate, self.balance.currency)
        # avoid zero-interest spam on tiny balances
        if incr.amount > 0:
            self.balance = self.balance + incr
            self._history.append(("INTEREST", incr))
