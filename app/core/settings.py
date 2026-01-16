from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Literal
import os
from pathlib import Path

ENV = Literal["local", "production"]


class AppSettings(BaseSettings):
    """
    Global application settings.

    Values are loaded in the following order:
    1. Environment variables
    2. .env file
    3. Defaults defined here
    """

    # -------------------------------------------------
    # Environment
    # -------------------------------------------------
    environment: ENV = Field(default="local", description="Deployment environment")

    # -------------------------------------------------
    # LangGraph / LangSmith
    # -------------------------------------------------
    langgraph_local_url: str = Field(
        default="http://127.0.0.1:2024", description="Local LangGraph server URL"
    )

    langgraph_production_url: str = Field(
        ..., description="Production LangGraph Cloud URL"
    )

    langsmith_api_key: str = Field(..., description="LangSmith API key")
    output_path: str | Path = Field(
        ..., description="Location to save any generated content"
    )

    # -------------------------------------------------
    # Derived / computed values
    # -------------------------------------------------
    @property
    def langgraph_url(self) -> str:
        """Return correct LangGraph URL for current environment."""
        return (
            self.langgraph_local_url
            if self.environment == "local"
            else self.langgraph_production_url
        )

    # -------------------------------------------------
    # Pydantic config
    # -------------------------------------------------
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# -------------------------------------------------
# Singleton accessor
# -------------------------------------------------


@lru_cache
def get_settings() -> AppSettings:
    """Cached settings instance (safe for Streamlit/FastAPI)."""
    return AppSettings(
        langgraph_production_url=os.getenv("langgraph_production", ""),
        langsmith_api_key=os.getenv("LANGSMITH_API_KEY", ""),
        output_path=Path("output_downloads").absolute(),
    )
