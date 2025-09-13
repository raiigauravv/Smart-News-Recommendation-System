from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "dev"
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]  # Vite dev

settings = Settings()