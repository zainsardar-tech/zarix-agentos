# ============================================================
#  Zarix AgentOS — Long-Term Memory (Vector Store)
# ============================================================
#  Persistent knowledge base backed by ChromaDB.
#  Stores embeddings of agent outputs, decisions, and learned
#  facts for semantic retrieval across sessions.
# ============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class LongTermMemory:
    """
    Vector-backed persistent memory using ChromaDB.

    Falls back gracefully to an in-memory store if ChromaDB is
    unavailable, so the system always works in development.
    """

    def __init__(self) -> None:
        self._collection = None
        self._fallback: list[dict] = []  # in-memory fallback
        self._init_collection()

    def _init_collection(self) -> None:
        """Initialise the ChromaDB collection."""
        try:
            import chromadb

            client = chromadb.HttpClient(
                host=settings.vector_db_url.replace("http://", "").replace("https://", "").split(":")[0],
                port=int(
                    settings.vector_db_url.replace("http://", "").replace("https://", "").split(":")[1]
                ),
            )
            self._collection = client.get_or_create_collection(
                name=settings.vector_db_collection,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info("Long-term memory connected to ChromaDB")
        except Exception as exc:
            logger.warning(
                "ChromaDB unavailable (%s) — using in-memory fallback", exc
            )
            self._collection = None

    async def store(
        self,
        content: str,
        agent_slug: Optional[str] = None,
        memory_type: str = "long_term",
        metadata: Optional[dict] = None,
    ) -> str:
        """Store a piece of knowledge and return its id."""
        doc_id = str(uuid.uuid4())
        meta = {
            "agent_slug": agent_slug or "system",
            "memory_type": memory_type,
            **(metadata or {}),
        }

        if self._collection is not None:
            try:
                self._collection.add(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[meta],
                )
                return doc_id
            except Exception as exc:
                logger.error("ChromaDB store failed: %s", exc)

        # Fallback
        self._fallback.append(
            {"id": doc_id, "content": content, "metadata": meta}
        )
        return doc_id

    async def search(
        self,
        query: str,
        agent_slug: Optional[str] = None,
        top_k: int = 5,
    ) -> list[str]:
        """Semantic search over stored knowledge."""
        if self._collection is not None:
            try:
                where = {"agent_slug": agent_slug} if agent_slug else None
                results = self._collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    where=where,
                )
                documents = results.get("documents", [[]])
                if documents and documents[0]:
                    return documents[0]
            except Exception as exc:
                logger.error("ChromaDB search failed: %s", exc)

        # Fallback: simple substring match
        matches = []
        query_lower = query.lower()
        for item in self._fallback:
            if agent_slug and item["metadata"].get("agent_slug") != agent_slug:
                continue
            if query_lower in item["content"].lower():
                matches.append(item["content"])
        return matches[:top_k]

    async def delete(self, doc_id: str) -> bool:
        """Delete a memory by id."""
        if self._collection is not None:
            try:
                self._collection.delete(ids=[doc_id])
                return True
            except Exception as exc:
                logger.error("ChromaDB delete failed: %s", exc)

        self._fallback = [m for m in self._fallback if m["id"] != doc_id]
        return True

    async def count(self) -> int:
        """Return the total number of stored memories."""
        if self._collection is not None:
            try:
                return self._collection.count()
            except Exception:
                pass
        return len(self._fallback)
