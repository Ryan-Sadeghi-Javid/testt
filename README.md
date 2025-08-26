# CLI OOP Banking System

## Goal
Model basic retail banking with clean OOP and a small CLI.

### Core Requirements
- Two account types: **Checking** and **Savings** (both inherit from `Account`).
- Operations: **open**, **deposit**, **withdraw**, **transfer**, **balance**, **statement**.
- Savings: monthly interest (simple compounding when `apply_interest` is called).
- Checking: optional overdraft protection flag/limit.
- All money handled with a `Money` value object (decimal, currency-aware).
- In-memory only (no DB). Collisions & validation must be handled.

### CLI Commands
- `open <type:checking|savings> <holder_name>`
- `deposit <account_id> <amount>`
- `withdraw <account_id> <amount>`
- `transfer <from_id> <to_id> <amount>`
- `balance <account_id>`
- `statement <account_id>`
- `apply_interest`  (applies to all savings accounts)

### Run
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.cli open checking "Alice"
