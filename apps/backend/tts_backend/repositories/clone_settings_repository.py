from __future__ import annotations

import sqlite3
from pathlib import Path

from ..schemas import CloneSetting, CloneSettingCreateRequest


class CloneSettingsRepository:
    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def initialize(self) -> None:
        self._database_path.parent.mkdir(parents=True, exist_ok=True)

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS clone_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    ref_audio_path TEXT NOT NULL,
                    ref_text TEXT NOT NULL,
                    lang TEXT NOT NULL,
                    speed REAL NOT NULL,
                    num_step INTEGER NOT NULL,
                    is_microphone_recording INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            columns = {
                str(row["name"])
                for row in connection.execute("PRAGMA table_info(clone_settings)").fetchall()
            }
            if "is_microphone_recording" not in columns:
                connection.execute(
                    "ALTER TABLE clone_settings ADD COLUMN is_microphone_recording INTEGER NOT NULL DEFAULT 0"
                )

    def create(self, request: CloneSettingCreateRequest, ref_audio_path: str) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO clone_settings (
                    name,
                    ref_audio_path,
                    ref_text,
                    lang,
                    speed,
                    num_step,
                    is_microphone_recording
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    request.name,
                    ref_audio_path,
                    request.ref_text,
                    request.lang,
                    request.speed,
                    request.num_step,
                    int(request.is_microphone_recording),
                ),
            )
            return int(cursor.lastrowid)

    def get(self, setting_id: int) -> CloneSetting | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, name, ref_audio_path, ref_text, lang, speed, num_step, is_microphone_recording, created_at
                FROM clone_settings
                WHERE id = ?
                """,
                (setting_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_clone_setting(row)

    def list(self) -> list[CloneSetting]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, name, ref_audio_path, ref_text, lang, speed, num_step, is_microphone_recording, created_at
                FROM clone_settings
                ORDER BY created_at DESC, id DESC
                """
            ).fetchall()

        return [self._row_to_clone_setting(row) for row in rows]

    def update(self, setting: CloneSetting) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE clone_settings
                SET name = ?, ref_audio_path = ?, ref_text = ?, lang = ?, speed = ?, num_step = ?, is_microphone_recording = ?
                WHERE id = ?
                """,
                (
                    setting.name,
                    setting.ref_audio_path,
                    setting.ref_text,
                    setting.lang,
                    setting.speed,
                    setting.num_step,
                    int(setting.is_microphone_recording),
                    setting.id,
                ),
            )

    def delete(self, setting_id: int) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM clone_settings WHERE id = ?", (setting_id,))

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _row_to_clone_setting(row: sqlite3.Row) -> CloneSetting:
        return CloneSetting(
            id=int(row["id"]),
            name=str(row["name"]),
            ref_audio_path=str(row["ref_audio_path"]),
            ref_text=str(row["ref_text"]),
            lang=str(row["lang"]),
            speed=float(row["speed"]),
            num_step=int(row["num_step"]),
            is_microphone_recording=bool(row["is_microphone_recording"]),
            created_at=str(row["created_at"]),
        )
