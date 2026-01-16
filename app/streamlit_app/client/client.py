from langgraph_sdk import get_client
from app.core.settings import get_settings


settings = get_settings()

if settings.environment == "local":
    client = get_client(
        url=settings.langgraph_local_url,
        api_key=settings.langsmith_api_key,
    )
else:
    client = get_client(
        url=settings.langgraph_production_url,
        api_key=settings.langsmith_api_key,
    )
