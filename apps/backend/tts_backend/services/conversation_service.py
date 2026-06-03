from __future__ import annotations

import sqlite3

from ..repositories.conversation_repository import ConversationRepository
from ..schemas import Conversation, ConversationUpsertRequest


class ConversationNotFoundError(LookupError):
    pass


class ConversationServiceError(RuntimeError):
    pass


class ConversationService:
    def __init__(self, repository: ConversationRepository) -> None:
        self._repository = repository

    def initialize(self) -> None:
        try:
            self._repository.initialize()
        except sqlite3.Error as exc:
            raise ConversationServiceError("Failed to initialize conversations.") from exc

    def create(self, request: ConversationUpsertRequest) -> Conversation:
        try:
            conversation_id = self._repository.create(request)
        except sqlite3.Error as exc:
            raise ConversationServiceError("Failed to create conversation.") from exc

        return self.get(conversation_id)

    def get(self, conversation_id: int) -> Conversation:
        try:
            conversation = self._repository.get(conversation_id)
        except sqlite3.Error as exc:
            raise ConversationServiceError("Failed to load conversation.") from exc

        if conversation is None:
            raise ConversationNotFoundError(f"Conversation {conversation_id} was not found.")

        return conversation

    def list(self) -> list[Conversation]:
        try:
            return self._repository.list()
        except sqlite3.Error as exc:
            raise ConversationServiceError("Failed to load conversations.") from exc

    def update(self, conversation_id: int, request: ConversationUpsertRequest) -> Conversation:
        self.get(conversation_id)

        try:
            self._repository.update(conversation_id, request)
        except sqlite3.Error as exc:
            raise ConversationServiceError("Failed to update conversation.") from exc

        return self.get(conversation_id)

    def delete(self, conversation_id: int) -> Conversation:
        conversation = self.get(conversation_id)

        try:
            self._repository.delete(conversation_id)
        except sqlite3.Error as exc:
            raise ConversationServiceError("Failed to delete conversation.") from exc

        return conversation
