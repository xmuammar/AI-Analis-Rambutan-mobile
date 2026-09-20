import hashlib
import hmac
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS trees (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    species TEXT NOT NULL DEFAULT 'Rambutan',
    variety TEXT NOT NULL DEFAULT 'Belereng',
    status TEXT NOT NULL DEFAULT 'SEHAT',
    notes TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS inspections (
    id INTEGER PRIMARY KEY,
    tree_id INTEGER NOT NULL REFERENCES trees(id),
    captured_at TEXT NOT NULL,
    condition TEXT NOT NULL,
    confidence REAL NOT NULL,
    evidence TEXT NOT NULL,
    surface_dark INTEGER NOT NULL DEFAULT 0,
    standing_water INTEGER NOT NULL DEFAULT 0,
    leaf_wilt INTEGER NOT NULL DEFAULT 0,
    moisture TEXT NOT NULL DEFAULT '',
    notes TEXT NOT NULL DEFAULT ''
);
"""


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def password_hash(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
    return f"{salt.hex()}${digest.hex()}"


def check_password(password: str, encoded: str) -> bool:
    try:
        salt_hex, digest_hex = encoded.split("$", 1)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt_hex), 120_000
        ).hex()
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(actual, digest_hex)


class LocalStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(SCHEMA)
        self._ensure_column("inspections", "photo_path", "TEXT NOT NULL DEFAULT ''")
        self._seed_trees()

    def _ensure_column(self, table: str, column: str, definition: str) -> None:
        columns = {
            row["name"]
            for row in self.connection.execute(f"PRAGMA table_info({table})")
        }
        if column not in columns:
            self.connection.execute(
                f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
            )
            self.connection.commit()

    def _seed_trees(self) -> None:
        if self.connection.execute("SELECT 1 FROM trees LIMIT 1").fetchone():
            return
        self.connection.executemany(
            "INSERT INTO trees(code) VALUES (?)",
            [(f"RBT-{number:03d}",) for number in range(1, 13)],
        )
        self.connection.commit()

    def register(self, username: str, password: str) -> None:
        self.connection.execute(
            "INSERT INTO users(username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, password_hash(password), utcnow()),
        )
        self.connection.commit()

    def authenticate(self, username: str, password: str) -> bool:
        row = self.connection.execute(
            "SELECT password_hash FROM users WHERE username = ?", (username,)
        ).fetchone()
        return row is not None and check_password(password, row["password_hash"])

    def trees(self):
        return self.connection.execute(
            "SELECT * FROM trees ORDER BY code"
        ).fetchall()

    def inspections(self, tree_id: int):
        return self.connection.execute(
            "SELECT * FROM inspections WHERE tree_id = ? ORDER BY captured_at DESC",
            (tree_id,),
        ).fetchall()

    def save_inspection(self, tree_id: int, values: dict) -> None:
        self.connection.execute(
            """
            INSERT INTO inspections(
                tree_id, captured_at, condition, confidence, evidence,
                surface_dark, standing_water, leaf_wilt, moisture, notes, photo_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tree_id,
                utcnow(),
                values["condition"],
                values["confidence"],
                values["evidence"],
                int(values["surface_dark"]),
                int(values["standing_water"]),
                int(values["leaf_wilt"]),
                values["moisture"],
                values["notes"],
                values.get("photo_path", ""),
            ),
        )
        self.connection.commit()

    def export_backup(self, destination: str | Path) -> Path:
        payload = {
            "format": "aianalisrambutan-offline",
            "version": 1,
            "exported_at": utcnow(),
            "trees": [dict(row) for row in self.trees()],
            "inspections": [
                dict(row)
                for row in self.connection.execute(
                    "SELECT * FROM inspections ORDER BY captured_at"
                )
            ],
        }
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        return destination

    def import_backup(self, source: str | Path) -> int:
        payload = json.loads(Path(source).read_text())
        if (
            payload.get("format") != "aianalisrambutan-offline"
            or payload.get("version") != 1
        ):
            raise ValueError("Format backup tidak didukung.")
        imported = 0
        for item in payload.get("inspections", []):
            exists = self.connection.execute(
                "SELECT 1 FROM inspections WHERE id = ?", (item.get("id"),)
            ).fetchone()
            if exists:
                continue
            tree_exists = self.connection.execute(
                "SELECT 1 FROM trees WHERE id = ?", (item.get("tree_id"),)
            ).fetchone()
            if not tree_exists:
                continue
            self.connection.execute(
                """
                INSERT INTO inspections(
                    id, tree_id, captured_at, condition, confidence, evidence,
                    surface_dark, standing_water, leaf_wilt, moisture, notes, photo_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["id"],
                    item["tree_id"],
                    item["captured_at"],
                    item["condition"],
                    item["confidence"],
                    item["evidence"],
                    item["surface_dark"],
                    item["standing_water"],
                    item["leaf_wilt"],
                    item["moisture"],
                    item["notes"],
                    item.get("photo_path", ""),
                ),
            )
            imported += 1
        self.connection.commit()
        return imported
