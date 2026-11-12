import sys
from pathlib import Path

from tabulate import tabulate

NAME = "Anna"
SURNAME = "Havula"
GROUP = "IT-32"

DATA_FILE = Path(__file__).resolve().parent / "data" / "expenses.csv"


def load_expenses(path):
    rows = []
    with path.open(encoding="utf-8-sig") as f:
        for number, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(";")
            try:
                if len(parts) < 3:
                    raise ValueError("expected at least 3 fields")
                category = parts[1].strip()
                amount = float(parts[2].strip().replace(",", "."))
                if not category or amount < 0:
                    raise ValueError("bad category or amount")
            except ValueError as err:
                print(f"warning: line {number} skipped ({err}): {line}",
                      file=sys.stderr)
                continue
            rows.append((category, amount))
    return rows


def main():
    print(f"{NAME} {SURNAME}, {GROUP}")

    try:
        expenses = load_expenses(DATA_FILE)
    except OSError as err:
        print(f"error: cannot read {DATA_FILE}: {err}", file=sys.stderr)
        sys.exit(1)
    if not expenses:
        print("error: no valid expenses found", file=sys.stderr)
        sys.exit(1)

    groups = {}
    for category, amount in expenses:
        entry = groups.setdefault(category, [0, 0.0])
        entry[0] += 1
        entry[1] += amount

    table = [[category, count, total] for category, (count, total) in groups.items()]
    table.append(["TOTAL",
                  sum(count for count, _ in groups.values()),
                  sum(total for _, total in groups.values())])

    print(tabulate(table, headers=["category", "count", "total"],
                   tablefmt="github", floatfmt=".2f"))


if __name__ == "__main__":
    main()