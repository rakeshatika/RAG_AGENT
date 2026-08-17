from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

# Always find .env relative to project root, regardless of where script is run from
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    LLM_API_KEY: str
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHAT_MODEL: str = "llama-3.3-70b-versatile"
    VECTOR_STORE_DIR: str = "data/vector_store"
    TOP_K: int = 3

    class Config:
        env_file = str(ENV_PATH)


@lru_cache()
def get_settings() -> Settings:
    return Settings()