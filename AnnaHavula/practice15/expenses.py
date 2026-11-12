import math
from pathlib import Path


def parse_line(line):
    parts = [part.strip() for part in line.strip().split(";")]
    if len(parts) != 4:
        raise ValueError(f"expected 4 fields, got {len(parts)}: {line!r}")

    date, category, amount_text, comment = parts
    try:
        amount = float(amount_text.replace(",", "."))
    except ValueError:
        raise ValueError(f"amount is not a number: {amount_text!r}") from None
    if not math.isfinite(amount):
        raise ValueError(f"amount is not a finite number: {amount_text!r}")

    return {"date": date, "category": category, "amount": amount, "comment": comment}


def total_by_category(records):
    totals = {}
    for record in records:
        category = record["category"]
        totals[category] = totals.get(category, 0.0) + record["amount"]
    return {category: round(total, 2) for category, total in totals.items()}


def load_expenses(path):
    records = []
    with Path(path).open(encoding="utf-8-sig") as f:
        for number, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                records.append(parse_line(line))
            except ValueError as err:
                raise ValueError(f"line {number}: {err}") from None
    return records