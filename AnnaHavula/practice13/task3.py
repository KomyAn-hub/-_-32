import math
import sys
from datetime import datetime
from pathlib import Path

NAME = "Anna"
SURNAME = "Havula"
GROUP = "IT-32"

UNITS = ["B", "KB", "MB", "GB"]
USAGE = "usage: python3 task3.py [--dry-run] <dir>"
SCRIPT_DIR = Path(__file__).resolve().parent


def human_size(size):
    if size <= 0:
        return "0.0 B"
    index = min(int(math.log(size, 1024) + 1e-9), len(UNITS) - 1)
    return f"{size / 1024 ** index:.1f} {UNITS[index]}"


def fail(message, code=1):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(code)


def main():
    print(f"{NAME} {SURNAME}, {GROUP}")

    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    rest = [a for a in args if a != "--dry-run"]
    if len(rest) != 1 or rest[0].startswith("--"):
        print(USAGE, file=sys.stderr)
        sys.exit(2)

    root = Path(rest[0])
    if not root.exists():
        fail(f"{root} does not exist")
    if not root.is_dir():
        fail(f"{root} is not a directory")

    started = datetime.now()

    plan = []
    try:
        for path in root.iterdir():
            if path.is_file():
                st = path.stat()
                modified = datetime.fromtimestamp(st.st_mtime)
                plan.append((modified, path, st.st_size,
                             modified.strftime("%Y-%m")))
    except OSError as err:
        fail(str(err))

    if not plan:
        print("no files to organize")
        return

    plan.sort(key=lambda item: (item[0], item[1].name))  # від старішого до новішого

    for _, path, _, folder in plan:
        subdir = root / folder
        target = subdir / path.name
        if subdir.exists() and not subdir.is_dir():
            fail(f"{subdir} exists and is not a directory, nothing was moved")
        if target.exists():
            fail(f"{target} already exists, nothing was moved")

    width = max(len(path.name) for _, path, _, _ in plan)
    lines = [f"{path.name:<{width}}  {human_size(size):>9}  "
             f"{modified:%d.%m.%Y %H:%M}  -> {folder}/"
             for modified, path, size, folder in plan]
    folders = {folder for _, _, _, folder in plan}
    summary = f"{len(plan)} files, {len(folders)} folders"

    for line in lines:
        print(line)

    if dry_run:
        print(summary + " (dry run, nothing moved)")
        return

    try:
        for _, path, _, folder in plan:
            subdir = root / folder
            subdir.mkdir(exist_ok=True)
            path.rename(subdir / path.name)
    except OSError as err:
        fail(f"move failed: {err}")
    print(summary)

    # Звіт
    reports_dir = SCRIPT_DIR / "reports"
    report_path = reports_dir / f"organize_{started:%Y%m%d_%H%M}.txt"
    try:
        reports_dir.mkdir(exist_ok=True)
        text = "\n".join([f"{NAME} {SURNAME}, {GROUP}",
                          f"started: {started:%d.%m.%Y %H:%M:%S}",
                          f"directory: {root}",
                          ""] + lines + [summary]) + "\n"
        report_path.write_text(text, encoding="utf-8")
    except OSError as err:
        fail(f"cannot save report: {err}")
    print(f"report saved to: {report_path.relative_to(SCRIPT_DIR).as_posix()}")


if __name__ == "__main__":
    main()