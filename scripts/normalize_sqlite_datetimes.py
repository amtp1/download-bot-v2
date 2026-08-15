"""Normalize uneven microsecond datetime strings in SQLite (from PG dumps)."""

import argparse
import sqlite3
from pathlib import Path


def normalize_datetime(value):
    if value is None:
        return None
    if not isinstance(value, str):
        return value

    text = value.replace("T", " ").strip()
    if "." not in text:
        return text

    head, frac = text.rsplit(".", 1)
    frac = "".join(ch for ch in frac if ch.isdigit())
    frac = (frac + "000000")[:6]
    return "{}.{}".format(head, frac)


def normalize_db(db_path):
    conn = sqlite3.connect(db_path)
    updated = 0
    try:
        for table, columns in (
            ("users", ("created", "updated")),
            ("downloads", ("created",)),
        ):
            for column in columns:
                rows = conn.execute(
                    "SELECT id, {0} FROM {1} WHERE {0} IS NOT NULL".format(column, table)
                ).fetchall()
                for row_id, value in rows:
                    new_value = normalize_datetime(value)
                    if new_value != value:
                        conn.execute(
                            "UPDATE {0} SET {1}=? WHERE id=?".format(table, column),
                            (new_value, row_id),
                        )
                        updated += 1
        conn.commit()
    finally:
        conn.close()
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("download_bot.db"),
        help="Path to SQLite database",
    )
    args = parser.parse_args()
    count = normalize_db(args.db)
    print("Normalized {} datetime values in {}".format(count, args.db.resolve()))


if __name__ == "__main__":
    main()
