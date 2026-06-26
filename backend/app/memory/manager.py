# ============================================================
#  Zarix AgentOS — Memory Manager
# ============================================================
#  Unified interface combining short-term (volatile) and
#  long-term (persistent vector) memory.
# ============================================================
from __future__ import annotations

import logging
from typing import Optional

from app.memory.long_term import LongTermMemory
from app.memory.short_term import ShortTermMemory

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Central memory manager used by every agent.

    Provides a clean API for storing and retrieving both
    short-term conversation context and long-term knowledge.
    """

    def __init__(self) -> None:
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()

    # ── Short-term ───────────────────────────────────────────

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        agent_slug: Optional[str] = None,
    ) -> None:
        """Add a message to the short-term conversation buffer."""
        self.short_term.add(session_id, role, content, agent_slug)

    def get_messages(self, session_id: str) -> list[dict]:
        """Retrieve the full short-term conversation."""
        return self.short_term.get(session_id)

    def get_recent_messages(self, session_id: str, n: int = 10) -> list[dict]:
        """Retrieve the last N messages."""
        return self.short_term.get_recent(session_id, n)

    async def add_short_term(
        self,
        agent_slug: str,
        content: str,
        task_id: str = "",
    ) -> None:
        """Convenience: store an agent's working output as short-term memory."""
        session = task_id or agent_slug
        self.short_term.add(session, "assistant", content, agent_slug)

    # ── Long-term ────────────────────────────────────────────

    async def add_long_term(
        self,
        agent_slug: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> str:
        """Persist knowledge to the long-term vector store."""
        doc_id = await self.long_term.store(
            content=content,
            agent_slug=agent_slug,
            memory_type="long_term",
            metadata=metadata,
        )
        logger.info(
            "Long-term memory stored by '%s' (id=%s)", agent_slug, doc_id
        )
        return doc_id

    async def search_long_term(
        self,
        query: str,
        agent_slug: Optional[str] = None,
        top_k: int = 5,
    ) -> list[str]:
        """Semantic search over long-term knowledge."""
        return await self.long_term.search(
            query=query,
            agent_slug=agent_slug,
            top_k=top_k,
        )

    async def delete_long_term(self, doc_id: str) -> bool:
        """Delete a long-term memory entry."""
        return await self.long_term.delete(doc_id)

    async def memory_count(self) -> int:
        """Total long-term memories stored."""
        return await self.long_term.count()

    # ── Combined ─────────────────────────────────────────────

    def clear_session(self, session_id: str) -> None:
        """Clear short-term memory for a session."""
        self.short_term.clear(session_id)
