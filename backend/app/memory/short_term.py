# ============================================================
#  Zarix AgentOS — Short-Term Memory
# ============================================================
#  In-process conversation buffer keyed by session/task.
#  Keeps the last N messages for each conversation.
# ============================================================
from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Optional


class ShortTermMemory:
    """
    Volatile, in-memory conversation store.

    Each session (identified by session_id / task_id) maintains a
    rolling window of the most recent messages.
    """

    def __init__(self, max_messages: int = 50) -> None:
        self.max_messages = max_messages
        self._store: dict[str, deque] = defaultdict(
            lambda: deque(maxlen=self.max_messages)
        )

    def add(
        self,
        session_id: str,
        role: str,
        content: str,
        agent_slug: Optional[str] = None,
    ) -> None:
        """Append a message to a session's buffer."""
        self._store[session_id].append(
            {
                "role": role,
                "content": content,
                "agent_slug": agent_slug,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    def get(self, session_id: str) -> list[dict]:
        """Return all messages for a session (oldest first)."""
        return list(self._store.get(session_id, []))

    def get_recent(self, session_id: str, n: int = 10) -> list[dict]:
        """Return the last N messages for a session."""
        messages = list(self._store.get(session_id, []))
        return messages[-n:] if n < len(messages) else messages

    def clear(self, session_id: str) -> None:
        """Remove all messages for a session."""
        self._store.pop(session_id, None)

    def clear_all(self) -> None:
        """Wipe all short-term memory."""
        self._store.clear()
