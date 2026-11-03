import math
import random
import sys
from datetime import datetime
from pathlib import Path

NAME = "Anna"
SURNAME = "Havula"
GROUP = "IT-32"
YEAR = 2009

HISTORY_FILE = Path(__file__).resolve().parent / "results" / "history.csv"
HEADER = "# datetime;score;seconds"
DT_FORMAT = "%Y-%m-%d %H:%M"


def make_tasks():
    tasks = []

    n = random.randint(2, 30)
    tasks.append((f"sqrt({n * n})", math.isqrt(n * n)))

    n = random.randint(3, 8)
    tasks.append((f"{n}!", math.factorial(n)))

    g = random.randint(2, 12)
    a, b = g * random.randint(2, 9), g * random.randint(2, 9)
    tasks.append((f"gcd({a}, {b})", math.gcd(a, b)))

    n = random.randint(5, 12)
    k = random.randint(2, n - 2)
    tasks.append((f"comb({n}, {k})", math.comb(n, k)))

    percent = random.choice([5, 10, 15, 20, 25, 30, 40, 50])
    base = random.randrange(20, 501, 20)
    tasks.append((f"{percent}% of {base}", percent * base // 100))

    return tasks


def ask(prompt):
    try:
        return input(prompt)
    except EOFError:
        return ""


def load_history(path):
    attempts = []
    if not path.exists():
        return attempts
    with path.open(encoding="utf-8") as f:
        for number, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                when_s, score_s, sec_s = line.split(";")
                attempts.append((datetime.strptime(when_s, DT_FORMAT),
                                 int(score_s), float(sec_s)))
            except ValueError:
                print(f"warning: history line {number} skipped: {line}",
                      file=sys.stderr)
    return attempts


def main():
    print(f"{NAME} {SURNAME}, {GROUP}")

    random.seed(YEAR)
    tasks = make_tasks()

    score = 0
    started = datetime.now()
    for number, (question, answer) in enumerate(tasks, 1):
        raw = ask(f"{number}) {question} = ")
        try:
            is_correct = int(raw.strip()) == answer
        except ValueError:
            is_correct = False
        if is_correct:
            score += 1
            print("   correct")
        else:
            print(f"   wrong, answer: {answer}")
    finished = datetime.now()

    seconds = (finished - started).total_seconds()
    print(f"score: {score}/{len(tasks)}, time: {seconds:.1f} s")

    try:
        HISTORY_FILE.parent.mkdir(exist_ok=True)
        is_new = not HISTORY_FILE.exists()
        with HISTORY_FILE.open("a", encoding="utf-8") as f:
            if is_new:
                f.write(HEADER + "\n")
            f.write(f"{finished.strftime(DT_FORMAT)};{score};{seconds:.1f}\n")
        attempts = load_history(HISTORY_FILE)
    except OSError as err:
        print(f"error: history file problem: {err}", file=sys.stderr)
        sys.exit(1)

    when, best_score, best_seconds = max(attempts, key=lambda a: (a[1], -a[2]))
    print(f"attempts: {len(attempts)}, best: {best_score}/{len(tasks)} "
          f"in {best_seconds:.1f} s ({when.strftime(DT_FORMAT)})")


if __name__ == "__main__":
    main()