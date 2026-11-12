from pathlib import Path

import qrcode

NAME = "Anna"
SURNAME = "Havula"
GROUP = "IT-32"
EMAIL = "annagaula92@gmail.com"

OUTPUT = Path(__file__).resolve().parent / "contact.png"


def main():
    print(f"{NAME} {SURNAME}, {GROUP}")

    text = f"{NAME} {SURNAME}, {GROUP}, {EMAIL}"
    image = qrcode.make(text)
    image.save(OUTPUT)
    print(f"saved: {OUTPUT.name}")
    print(f"text: {text}")


if __name__ == "__main__":
    main()