from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings model from environment"""

    NEO4J_URI: str
    NEO4J_USERNAME: str = ""
    NEO4J_PASSWORD: str = ""


settings = Settings()  # type: ignore
