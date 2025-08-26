import pytest
from src.money import Money
from src.account import CheckingAccount, SavingsAccount
from src.errors import InsufficientFunds

def test_checking_overdraft_allowed():
    c = CheckingAccount(id="1", holder="A", balance=Money.parse("10.00"), overdraft_limit=Money.parse("50.00"))
    c.withdraw(Money.parse("55.00"))  # balance becomes -45.00
    assert str(c.balance) == "CAD -45.00"

def test_savings_interest_applies():
    s = SavingsAccount(id="2", holder="B", balance=Money.parse("100.00"), annual_interest_rate_bps=1200)  # 12%
    s.apply_monthly_interest()
    # ~1% of 100 = 1.00
    assert s.balance.amount >= Money.parse("101.00").amount

def test_withdraw_blocks_without_overdraft():
    c = CheckingAccount(id="3", holder="C", balance=Money.parse("10.00"))
    with pytest.raises(InsufficientFunds):
        c.withdraw(Money.parse("20.00"))

