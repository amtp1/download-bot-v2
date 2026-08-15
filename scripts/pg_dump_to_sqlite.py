"""Convert PostgreSQL pg_dump (COPY format) to a SQLite database."""

import argparse
import re
import sqlite3
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

COPY_RE = re.compile(
    r"^COPY public\.(?P<table>\w+) \((?P<columns>[^)]+)\) FROM stdin;\s*$"
)


def unescape_pg(value: str) -> Optional[str]:
    if value == r"\N":
        return None

    out = []  # type: List[str]
    i = 0
    while i < len(value):
        ch = value[i]
        if ch == "\\" and i + 1 < len(value):
            nxt = value[i + 1]
            mapping = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "\\": "\\"}
            out.append(mapping.get(nxt, nxt))
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def parse_bool(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    if value in {"t", "true", "1"}:
        return 1
    if value in {"f", "false", "0"}:
        return 0
    raise ValueError("Unexpected boolean value: {!r}".format(value))


def normalize_datetime(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = value.replace("T", " ").strip()
    if "." in text:
        head, frac = text.rsplit(".", 1)
        frac = "".join(ch for ch in frac if ch.isdigit())
        frac = (frac + "000000")[:6]
        text = "{}.{}".format(head, frac)
    return text


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA foreign_keys = OFF;

        DROP TABLE IF EXISTS alembic_version;
        DROP TABLE IF EXISTS downloads;
        DROP TABLE IF EXISTS users;

        CREATE TABLE alembic_version (
            version_num VARCHAR(32) NOT NULL PRIMARY KEY
        );

        CREATE TABLE downloads (
            id INTEGER NOT NULL PRIMARY KEY,
            user_id INTEGER,
            link VARCHAR,
            content_type VARCHAR,
            service VARCHAR,
            created DATETIME
        );

        CREATE TABLE users (
            id INTEGER NOT NULL PRIMARY KEY,
            role VARCHAR,
            user_id INTEGER,
            username VARCHAR,
            first_name VARCHAR NOT NULL,
            last_name VARCHAR,
            download_count VARCHAR,
            updated DATETIME,
            created DATETIME,
            is_blocked BOOLEAN
        );
        """
    )


def convert_row(table: str, columns: List[str], raw_fields: List[str]) -> Tuple:
    values = [unescape_pg(field) for field in raw_fields]
    if len(values) != len(columns):
        raise ValueError(
            "Column count mismatch in {}: expected {}, got {}".format(
                table, len(columns), len(values)
            )
        )

    if table == "users" and "is_blocked" in columns:
        idx = columns.index("is_blocked")
        values[idx] = parse_bool(values[idx])

    for col in ("created", "updated"):
        if col in columns:
            idx = columns.index(col)
            values[idx] = normalize_datetime(values[idx])

    return tuple(values)


def iter_copy_blocks(sql_path: Path) -> Iterator[Tuple[str, List[str], List[Tuple]]]:
    with sql_path.open("r", encoding="utf-8") as handle:
        table = None
        columns = []  # type: List[str]
        rows = []  # type: List[Tuple]

        for line in handle:
            if table is None:
                match = COPY_RE.match(line)
                if not match:
                    continue
                table = match.group("table")
                columns = [c.strip() for c in match.group("columns").split(",")]
                rows = []
                continue

            if line.rstrip("\n") == r"\.":
                yield table, columns, rows
                table = None
                columns = []
                rows = []
                continue

            raw_fields = line.rstrip("\n").split("\t")
            rows.append(convert_row(table, columns, raw_fields))


def convert(sql_path: Path, db_path: Path) -> Dict[str, int]:
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        create_schema(conn)
        counts = {}  # type: Dict[str, int]

        for table, columns, rows in iter_copy_blocks(sql_path):
            placeholders = ", ".join("?" for _ in columns)
            col_list = ", ".join(columns)
            conn.executemany(
                "INSERT INTO {} ({}) VALUES ({})".format(table, col_list, placeholders),
                rows,
            )
            counts[table] = len(rows)

        conn.commit()
        return counts
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sql",
        type=Path,
        default=Path("download_bot.sql"),
        help="Path to PostgreSQL dump",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("download_bot.db"),
        help="Output SQLite database path",
    )
    args = parser.parse_args()

    counts = convert(args.sql, args.db)
    print("Created {}".format(args.db.resolve()))
    for table, count in counts.items():
        print("  {}: {} rows".format(table, count))


if __name__ == "__main__":
    main()
