from pathlib import Path

import pytest

from expenses import load_expenses, parse_line, total_by_category

REAL_FILE = Path(__file__).resolve().parent / "data" / "expenses.csv"

REAL_ROWS = [
    ("2026-09-21;food;85.50;lunch", "food", 85.5),
    ("2026-09-21;transport;32.00;bus", "transport", 32.0),
    ("2026-09-23;fun;250.00;cinema", "fun", 250.0),
    ("2026-09-25;food;120.00;lunch", "food", 120.0),
    ("2026-09-26;transport;50.00;taxi", "transport", 50.0),
]
REAL_TOTALS = {"food": 642.5, "transport": 210.0, "fun": 395.5}

def test_parse_line_valid():
    record = parse_line("2026-09-21;food;85.50;lunch")
    assert record["category"] == "food"
    assert record["amount"] == 85.5


def test_parse_line_returns_full_record():
    assert parse_line("2026-09-21;food;85.50;lunch") == {
        "date": "2026-09-21",
        "category": "food",
        "amount": 85.5,
        "comment": "lunch",
    }


def test_parse_line_amount_is_float():
    assert isinstance(parse_line("2026-09-21;food;85;lunch")["amount"], float)


def test_parse_line_comma_decimal_and_spaces():
    record = parse_line(" 2026-09-21 ; food ; 85,50 ; lunch \n")
    assert record["category"] == "food"
    assert record["amount"] == 85.5


def test_parse_line_bad_amount():
    with pytest.raises(ValueError):
        parse_line("2026-09-21;food;abc;lunch")


def test_parse_line_too_few_fields():
    with pytest.raises(ValueError):
        parse_line("2026-09-21;food;85.50")


def test_parse_line_too_many_fields():
    with pytest.raises(ValueError):
        parse_line("2026-09-21;food;85.50;lunch;extra")


def test_parse_line_empty_amount():
    with pytest.raises(ValueError):
        parse_line("2026-09-21;food;;lunch")


def test_parse_line_error_message():
    with pytest.raises(ValueError, match="not a number"):
        parse_line("2026-09-21;food;abc;lunch")


@pytest.mark.parametrize("line, category, amount", REAL_ROWS)
def test_parse_line_real_rows(line, category, amount):
    record = parse_line(line)
    assert record["category"] == category
    assert record["amount"] == amount


def test_total_by_category(tmp_path):
    path = tmp_path / "expenses.csv"
    path.write_text(
        "# date;category;amount;comment\n"
        "2026-09-21;food;85.50;lunch\n"
        "\n"
        "2026-09-22;food;14.50;coffee\n",
        encoding="utf-8",
    )
    totals = total_by_category(load_expenses(path))
    assert totals == {"food": 100.0}


def test_total_by_category_rounds_to_two_decimals():
    records = [
        {"category": "food", "amount": 0.1},
        {"category": "food", "amount": 0.2},
    ]
    assert total_by_category(records) == {"food": 0.3}


def test_load_expenses_reports_line_number(tmp_path):
    path = tmp_path / "expenses.csv"
    path.write_text("2026-09-21;food;85.50;lunch\n2026-09-22;food;abc;x\n",
                    encoding="utf-8")
    with pytest.raises(ValueError, match="line 2"):
        load_expenses(path)


def test_total_by_category_real_file():
    assert total_by_category(load_expenses(REAL_FILE)) == REAL_TOTALS