import sys
from .bank import Bank
from .money import Money

def main():
    bank = Bank()
    args = sys.argv[1:]
    if not args:
        print("Usage: python -m src.cli <command> [...]"); return

    cmd = args[0]
    try:
        if cmd == "open":
            _, kind, holder = args  # open <checking|savings> <holder>
            acc_id = bank.open_account(kind, holder)
            print(acc_id)
        elif cmd == "deposit":
            _, acc, amt = args
            bank.deposit(acc, Money.parse(amt))
            print("OK")
        elif cmd == "withdraw":
            _, acc, amt = args
            bank.withdraw(acc, Money.parse(amt))
            print("OK")
        elif cmd == "transfer":
            _, src, dst, amt = args
            bank.transfer(src, dst, Money.parse(amt))
            print("OK")
        elif cmd == "balance":
            _, acc = args
            print(bank.get(acc).balance)
        elif cmd == "statement":
            _, acc = args
            print(bank.get(acc).statement())
        elif cmd == "apply_interest":
            bank.apply_interest()
            print("OK")
        else:
            print(f"Unknown command: {cmd}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
