# ============================================================
#  Zarix AgentOS — Settings (Pydantic Settings)
# ============================================================
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────
    app_name: str = "Zarix AgentOS"
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_log_level: str = "INFO"
    secret_key: str = "change-me-to-a-long-random-string"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    # ── Database ─────────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://zarix:zarix@localhost:5432/zarix_agentos"
    redis_url: str = "redis://localhost:6379/0"

    # ── Vector DB ────────────────────────────────────────────
    vector_db_type: str = "chroma"
    vector_db_url: str = "http://localhost:8001"
    vector_db_collection: str = "zarix_memory"

    # ── LLM Provider Keys ───────────────────────────────────
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    meta_api_key: str = ""
    meta_base_url: str = "https://api.together.xyz/v1"
    mistral_api_key: str = ""
    deepseek_api_key: str = ""

    # ── Default LLM ──────────────────────────────────────────
    default_llm_provider: str = "anthropic"
    default_llm_model: str = "claude-sonnet"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 4096
    llm_timeout: int = 120

    # ── Tools / Sandbox ──────────────────────────────────────
    enable_code_execution: bool = True
    enable_web_search: bool = True
    enable_shell_access: bool = False
    sandbox_timeout: int = 60

    # ── Frontend ─────────────────────────────────────────────
    next_public_api_url: str = "http://localhost:8000"
    next_public_ws_url: str = "ws://localhost:8000/ws"

    # ── Convenience helpers ──────────────────────────────────
    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    def get_provider_key(self, provider: str) -> str:
        """Return the API key for a given provider name."""
        mapping = {
            "openai": self.openai_api_key,
            "anthropic": self.anthropic_api_key,
            "google": self.google_api_key,
            "meta": self.meta_api_key,
            "mistral": self.mistral_api_key,
            "deepseek": self.deepseek_api_key,
        }
        return mapping.get(provider.lower(), "")


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()


settings = get_settings()
