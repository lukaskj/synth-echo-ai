from __future__ import annotations

import sqlite3
from pathlib import Path

from ..schemas import Conversation, ConversationLine, ConversationLineUpsertRequest, ConversationUpsertRequest


class ConversationRepository:
    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def initialize(self) -> None:
        self._database_path.parent.mkdir(parents=True, exist_ok=True)

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS conversation_lines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    position INTEGER NOT NULL,
                    text TEXT NOT NULL DEFAULT '',
                    voice_type TEXT NOT NULL,
                    clone_setting_id INTEGER,
                    voice_label TEXT NOT NULL,
                    audio_url TEXT NOT NULL DEFAULT '',
                    lang TEXT NOT NULL,
                    speed REAL NOT NULL,
                    num_step INTEGER NOT NULL,
                    instruct TEXT NOT NULL DEFAULT '',
                    selected_gender TEXT NOT NULL DEFAULT '',
                    selected_accent TEXT NOT NULL DEFAULT '',
                    selected_pitch TEXT NOT NULL DEFAULT '',
                    selected_age TEXT NOT NULL DEFAULT '',
                    selected_style TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_conversation_lines_conversation_position
                ON conversation_lines (conversation_id, position, id)
                """
            )

    def create(self, request: ConversationUpsertRequest) -> int:
        with self._connect() as connection:
            cursor = connection.execute("INSERT INTO conversations (name) VALUES (?)", (request.name,))
            conversation_id = int(cursor.lastrowid)
            self._replace_lines(connection, conversation_id, request.lines)
            return conversation_id

    def get(self, conversation_id: int) -> Conversation | None:
        with self._connect() as connection:
            conversation_row = connection.execute(
                """
                SELECT id, name, created_at, updated_at
                FROM conversations
                WHERE id = ?
                """,
                (conversation_id,),
            ).fetchone()
            if conversation_row is None:
                return None

            line_rows = connection.execute(
                """
                SELECT id, conversation_id, position, text, voice_type, clone_setting_id, voice_label,
                       audio_url, lang, speed, num_step, instruct, selected_gender, selected_accent,
                       selected_pitch, selected_age, selected_style, created_at, updated_at
                FROM conversation_lines
                WHERE conversation_id = ?
                ORDER BY position ASC, id ASC
                """,
                (conversation_id,),
            ).fetchall()

        return self._row_to_conversation(conversation_row, line_rows)

    def list(self) -> list[Conversation]:
        with self._connect() as connection:
            conversation_rows = connection.execute(
                """
                SELECT id, name, created_at, updated_at
                FROM conversations
                ORDER BY updated_at DESC, id DESC
                """
            ).fetchall()
            line_rows = connection.execute(
                """
                SELECT id, conversation_id, position, text, voice_type, clone_setting_id, voice_label,
                       audio_url, lang, speed, num_step, instruct, selected_gender, selected_accent,
                       selected_pitch, selected_age, selected_style, created_at, updated_at
                FROM conversation_lines
                ORDER BY conversation_id ASC, position ASC, id ASC
                """
            ).fetchall()

        lines_by_conversation_id: dict[int, list[sqlite3.Row]] = {}
        for row in line_rows:
            conversation_id = int(row["conversation_id"])
            lines_by_conversation_id.setdefault(conversation_id, []).append(row)

        return [
            self._row_to_conversation(row, lines_by_conversation_id.get(int(row["id"]), []))
            for row in conversation_rows
        ]

    def update(self, conversation_id: int, request: ConversationUpsertRequest) -> None:
        with self._connect() as connection:
            connection.execute(
                "UPDATE conversations SET name = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (request.name, conversation_id),
            )
            self._replace_lines(connection, conversation_id, request.lines)

    def delete(self, conversation_id: int) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))

    def _replace_lines(
        self,
        connection: sqlite3.Connection,
        conversation_id: int,
        lines: tuple[ConversationLineUpsertRequest, ...],
    ) -> None:
        connection.execute("DELETE FROM conversation_lines WHERE conversation_id = ?", (conversation_id,))

        for position, line in enumerate(sorted(lines, key=lambda item: item.position)):
            connection.execute(
                """
                INSERT INTO conversation_lines (
                    conversation_id,
                    position,
                    text,
                    voice_type,
                    clone_setting_id,
                    voice_label,
                    audio_url,
                    lang,
                    speed,
                    num_step,
                    instruct,
                    selected_gender,
                    selected_accent,
                    selected_pitch,
                    selected_age,
                    selected_style
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    conversation_id,
                    position,
                    line.text,
                    line.voice_type,
                    line.clone_setting_id,
                    line.voice_label,
                    line.audio_url,
                    line.lang,
                    line.speed,
                    line.num_step,
                    line.instruct,
                    line.selected_gender,
                    line.selected_accent,
                    line.selected_pitch,
                    line.selected_age,
                    line.selected_style,
                ),
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @staticmethod
    def _row_to_conversation(conversation_row: sqlite3.Row, line_rows: list[sqlite3.Row]) -> Conversation:
        return Conversation(
            id=int(conversation_row["id"]),
            name=str(conversation_row["name"]),
            lines=tuple(ConversationRepository._row_to_conversation_line(row) for row in line_rows),
            created_at=str(conversation_row["created_at"]),
            updated_at=str(conversation_row["updated_at"]),
        )

    @staticmethod
    def _row_to_conversation_line(row: sqlite3.Row) -> ConversationLine:
        return ConversationLine(
            id=int(row["id"]),
            conversation_id=int(row["conversation_id"]),
            position=int(row["position"]),
            text=str(row["text"]),
            voice_type=str(row["voice_type"]),
            clone_setting_id=int(row["clone_setting_id"]) if row["clone_setting_id"] is not None else None,
            voice_label=str(row["voice_label"]),
            audio_url=str(row["audio_url"]),
            lang=str(row["lang"]),
            speed=float(row["speed"]),
            num_step=int(row["num_step"]),
            instruct=str(row["instruct"]),
            selected_gender=str(row["selected_gender"]),
            selected_accent=str(row["selected_accent"]),
            selected_pitch=str(row["selected_pitch"]),
            selected_age=str(row["selected_age"]),
            selected_style=str(row["selected_style"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )
