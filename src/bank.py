from typing import Dict
from .money import Money
from .account import Account, CheckingAccount, SavingsAccount
from .errors import AccountNotFound, InvalidOperation

class Bank:
    def __init__(self):
        self._accounts: Dict[str, Account] = {}
        self._next_id = 1

    def open_account(self, kind: str, holder: str) -> str:
        account_id = str(self._next_id); self._next_id += 1
        if kind.lower() == "checking":
            acct = CheckingAccount(id=account_id, holder=holder, balance=Money.parse("0.00"))
        elif kind.lower() == "savings":
            acct = SavingsAccount(id=account_id, holder=holder, balance=Money.parse("0.00"))
        else:
            raise InvalidOperation("Unknown account type")
        self._accounts[account_id] = acct
        return account_id

    def get(self, account_id: str) -> Account:
        acct = self._accounts.get(account_id)
        if not acct:
            raise AccountNotFound(account_id)
        return acct

    def deposit(self, account_id: str, amount: Money):
        self.get(account_id).deposit(amount)

    def withdraw(self, account_id: str, amount: Money):
        self.get(account_id).withdraw(amount)

    def transfer(self, from_id: str, to_id: str, amount: Money):
        src = self.get(from_id)
        dst = self.get(to_id)
        src.transfer_out(amount)
        dst.transfer_in(amount)

    def apply_interest(self):
        # apply to all savings
        for acct in self._accounts.values():
            if isinstance(acct, SavingsAccount):
                acct.apply_monthly_interest()