"""Generate the markdown lists from the CSV files in this folder and write them
into the README, between the list-start and list-end markers.

Usage: python data/generate_lists.py
"""

import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent
README = DATA_DIR.parent / "README.md"
START_MARKER = "<!-- list-start -->"
END_MARKER = "<!-- list-end -->"

SECTIONS = [
    ("Qompanies", "companies.csv"),
    ("ProjeQts", "projects.csv"),
]


def to_markdown_name(name):
    """Bold every capital Q in the name."""
    return name.replace("Q", "**Q**")


def format_entry(row):
    name = to_markdown_name(row["name"])
    emojis = "|".join(row["emojis"].split())
    return f"- [{name}]({row['url']}) {row['flag']} - {row['description']}. {emojis}".rstrip()


def generate_section(title, filename):
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        rows = sorted(csv.DictReader(f), key=lambda row: row["name"].casefold())
    lines = [f"## {title}"] + [format_entry(row) for row in rows]
    return "\n".join(lines)


def update_readme(content):
    """Replace everything between the markers in the README with content."""
    text = README.read_text(encoding="utf-8")
    start = text.index(START_MARKER) + len(START_MARKER)
    end = text.index(END_MARKER)
    README.write_text(f"{text[:start]}\n{content}\n{text[end:]}", encoding="utf-8")


def main():
    update_readme("\n\n".join(generate_section(t, f) for t, f in SECTIONS))


if __name__ == "__main__":
    main()
