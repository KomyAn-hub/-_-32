"""Лабораторна 30, завдання 2. Коли ви витрачаєте гроші."""
import math
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

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
                day = datetime.strptime(parts[0].strip(), "%Y-%m-%d").date()
                amount = float(parts[2].strip().replace(",", "."))
                if not math.isfinite(amount) or amount < 0:
                    raise ValueError("bad amount")
            except ValueError as err:
                print(f"warning: line {number} skipped ({err}): {line}",
                      file=sys.stderr)
                continue
            rows.append((day, amount))
    return rows


def days_in_month(d):
    first = d.replace(day=1)
    next_first = (first + timedelta(days=32)).replace(day=1)
    return (next_first - first).days


def selftest():
    cases = [(date(2026, 12, 15), 31),
             (date(2028, 2, 10), 29),
             (date(2026, 2, 10), 28),
             (date(2026, 9, 27), 30)]
    for d, expected in cases:
        got = days_in_month(d)
        status = "ok" if got == expected else "FAIL"
        print(f"{d}: {got} (expected {expected}) {status}")
        if got != expected:
            sys.exit(1)


def main():
    print(f"{NAME} {SURNAME}, {GROUP}")

    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
        return

    try:
        rows = load_expenses(DATA_FILE)
    except OSError as err:
        print(f"error: cannot read {DATA_FILE}: {err}", file=sys.stderr)
        sys.exit(1)
    if not rows:
        print("error: no valid expenses found", file=sys.stderr)
        sys.exit(1)

    by_day = {}
    for day, amount in rows:
        by_day.setdefault(day, []).append(amount)

    first, last = min(by_day), max(by_day)
    span = (last - first).days + 1

    daily = []
    for i in range(span):
        d = first + timedelta(days=i)
        daily.append((d, math.fsum(by_day.get(d, []))))

    print(f"period: {first:%d.%m.%Y} ({first:%A}) - "
          f"{last:%d.%m.%Y} ({last:%A}), {span} days")
    print()

    monday = date(2024, 1, 1)
    names = [(monday + timedelta(days=i)).strftime("%A") for i in range(7)]
    per_weekday = [[] for _ in range(7)]
    for d, s in daily:
        per_weekday[d.weekday()].append(s)

    print(f"{'weekday':<9}{'total':>10}")
    for name, values in zip(names, per_weekday):
        print(f"{name:<9}{math.fsum(values):>10.2f}")
    print()

    total = math.fsum(s for _, s in daily)
    mean = total / span
    std = math.sqrt(math.fsum((s - mean) ** 2 for _, s in daily) / span)
    top_day, top_sum = max(daily, key=lambda item: item[1])
    no_spend = sum(1 for _, s in daily if s == 0)

    print(f"{'total:':<14}{total:.2f}")
    print(f"{'per day:':<14}{mean:.2f} +- {std:.2f}")
    print(f"{'top day:':<14}{top_day:%d.%m.%Y} ({top_day:%A}), {top_sum:.2f}")
    print(f"{'no-spend days:':<14} {no_spend}")

    month_days = days_in_month(last)
    left = month_days - last.day
    print(f"days in {last:%B}: {month_days}, left after {last:%d.%m}: {left}")
    print(f"month forecast: {mean * month_days:.2f}")


if __name__ == "__main__":
    main()