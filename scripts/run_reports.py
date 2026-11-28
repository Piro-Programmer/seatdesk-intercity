"""Run the five reports in sql/reports.sql against seatdesk.db and print each result as a table.

Usage: python scripts/run_reports.py [path/to/seatdesk.db]
"""
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def split_reports(sql_text):
    """Return [(label, query), ...] using the '-- R<n>:' label lines."""
    parts = re.split(r"^-- (R\d):.*$", sql_text, flags=re.MULTILINE)
    return [(parts[i], parts[i + 1].strip()) for i in range(1, len(parts), 2)]


def print_table(label, cursor, rows):
    headers = [d[0] for d in cursor.description]
    print(f"{label} - {len(rows)} rows")
    print("| " + " | ".join(headers) + " |")
    print("|" + "---|" * len(headers))
    for row in rows:
        print("| " + " | ".join(str(v) for v in row) + " |")
    print()


def main():
    db_path = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "seatdesk.db")
    conn = sqlite3.connect(db_path)
    sql_text = (ROOT / "sql" / "reports.sql").read_text(encoding="utf-8")
    for label, query in split_reports(sql_text):
        cur = conn.execute(query)
        print_table(label, cur, cur.fetchall())
    conn.close()


if __name__ == "__main__":
    main()
