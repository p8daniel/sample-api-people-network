import uvicorn
from pydantic_settings import BaseSettings

from app.core.log_configuration import load_log_configuration


class ServerSettings(BaseSettings):
    """Server settings model"""

    API_AUTORELOAD: bool = False
    API_PORT: int = 5000


settings = ServerSettings()

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",  # nosec
        reload=settings.API_AUTORELOAD,
        port=settings.API_PORT,
        log_config=load_log_configuration(),
    )
